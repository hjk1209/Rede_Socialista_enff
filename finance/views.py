import csv
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.views import View
from django.views.generic import TemplateView

from .forms import (
    FinanceAccountForm,
    FinanceBudgetForm,
    FinanceBudgetLineForm,
    FinanceBudgetReviewForm,
    FinanceContributionForm,
    FinanceExpenseDecisionForm,
    FinanceExpenseForm,
)
from .models import (
    FinanceAccount,
    FinanceBudget,
    FinanceBudgetLine,
    FinanceBudgetReview,
    FinanceContribution,
    FinanceExpense,
    FinanceExpenseDecision,
)


def can_manage_finance(user):
    return bool(getattr(user, 'can_operate_finance', False))


class FinanceOperatorRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not can_manage_finance(request.user):
            messages.error(request, 'A area financeira e reservada para operadores autorizados.')
            return redirect('feed')
        return super().dispatch(request, *args, **kwargs)


def money_sum(queryset, field='amount'):
    return queryset.aggregate(total=Sum(field))['total'] or Decimal('0.00')


def account_balance(account):
    income = money_sum(account.contributions.all())
    paid = money_sum(account.expenses.filter(status=FinanceExpense.Status.PAID))
    return account.opening_balance + income - paid


class FinanceDashboardView(FinanceOperatorRequiredMixin, TemplateView):
    template_name = 'finance/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.localdate()
        month_start = today.replace(day=1)
        accounts = FinanceAccount.objects.filter(is_active=True).prefetch_related('contributions', 'expenses')
        budgets = FinanceBudget.objects.prefetch_related('lines', 'expenses')[:12]
        expenses = FinanceExpense.objects.select_related('budget', 'account', 'requested_by', 'approved_by', 'paid_by')[:18]
        contributions = FinanceContribution.objects.select_related('account', 'recorded_by')[:12]

        context['account_form'] = kwargs.get('account_form') or FinanceAccountForm()
        context['budget_form'] = kwargs.get('budget_form') or FinanceBudgetForm()
        context['budget_line_form'] = kwargs.get('budget_line_form') or FinanceBudgetLineForm()
        context['expense_form'] = kwargs.get('expense_form') or FinanceExpenseForm()
        context['contribution_form'] = kwargs.get('contribution_form') or FinanceContributionForm()
        context['budget_review_form'] = FinanceBudgetReviewForm()
        context['expense_decision_form'] = FinanceExpenseDecisionForm()
        context['accounts'] = [
            {
                'instance': account,
                'balance': account_balance(account),
            }
            for account in accounts
        ]
        context['budgets'] = [
            {
                'instance': budget,
                'spent_total': money_sum(budget.expenses.filter(status__in=[
                    FinanceExpense.Status.APPROVED,
                    FinanceExpense.Status.PAID,
                ])),
                'paid_total': money_sum(budget.expenses.filter(status=FinanceExpense.Status.PAID)),
                'line_total': money_sum(budget.lines.all(), field='planned_amount'),
            }
            for budget in budgets
        ]
        context['expenses'] = expenses
        context['contributions'] = contributions
        context['income_month_total'] = money_sum(FinanceContribution.objects.filter(received_at__gte=month_start))
        context['paid_month_total'] = money_sum(
            FinanceExpense.objects.filter(status=FinanceExpense.Status.PAID, payment_date__gte=month_start)
        )
        context['pending_expense_total'] = money_sum(
            FinanceExpense.objects.filter(status__in=[FinanceExpense.Status.REQUESTED, FinanceExpense.Status.REVIEW])
        )
        context['approved_budget_total'] = money_sum(
            FinanceBudget.objects.filter(status=FinanceBudget.Status.APPROVED),
            field='total_planned',
        )
        context['cash_total'] = sum((item['balance'] for item in context['accounts']), Decimal('0.00'))
        return context


class FinanceAccountCreateView(FinanceOperatorRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        form = FinanceAccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.created_by = request.user
            account.save()
            messages.success(request, f'Conta/caixa {account.name} cadastrada.')
        else:
            for field_errors in form.errors.values():
                for error in field_errors:
                    messages.error(request, error)
        return redirect('finance-dashboard')


class FinanceBudgetCreateView(FinanceOperatorRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        form = FinanceBudgetForm(request.POST)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.created_by = request.user
            budget.save()
            messages.success(request, f'Orcamento {budget.title} criado como rascunho.')
        else:
            for field_errors in form.errors.values():
                for error in field_errors:
                    messages.error(request, error)
        return redirect('finance-dashboard')


class FinanceBudgetLineCreateView(FinanceOperatorRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        form = FinanceBudgetLineForm(request.POST)
        if form.is_valid():
            line = form.save()
            messages.success(request, f'Linha adicionada ao orcamento {line.budget.title}.')
        else:
            for field_errors in form.errors.values():
                for error in field_errors:
                    messages.error(request, error)
        return redirect('finance-dashboard')


class FinanceBudgetSubmitView(FinanceOperatorRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        budget = get_object_or_404(FinanceBudget, pk=pk)
        if budget.status not in {FinanceBudget.Status.DRAFT, FinanceBudget.Status.REJECTED}:
            messages.info(request, 'Este orcamento nao pode ser reenviado agora.')
            return redirect('finance-dashboard')
        budget.status = FinanceBudget.Status.SUBMITTED
        budget.submitted_at = timezone.now()
        budget.save(update_fields=['status', 'submitted_at', 'updated_at'])
        messages.success(request, f'Orcamento {budget.title} enviado para aprovacao.')
        return redirect('finance-dashboard')


class FinanceBudgetReviewView(FinanceOperatorRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        budget = get_object_or_404(FinanceBudget, pk=pk)
        form = FinanceBudgetReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.budget = budget
            review.reviewer = request.user
            review.save()
            if review.decision == FinanceBudgetReview.Decision.APPROVED:
                budget.status = FinanceBudget.Status.APPROVED
            elif review.decision == FinanceBudgetReview.Decision.REJECTED:
                budget.status = FinanceBudget.Status.REJECTED
            else:
                budget.status = FinanceBudget.Status.DRAFT
            budget.reviewed_by = request.user
            budget.reviewed_at = timezone.now()
            budget.save(update_fields=['status', 'reviewed_by', 'reviewed_at', 'updated_at'])
            messages.success(request, f'Parecer registrado para {budget.title}.')
        else:
            for field_errors in form.errors.values():
                for error in field_errors:
                    messages.error(request, error)
        return redirect('finance-dashboard')


class FinanceExpenseCreateView(FinanceOperatorRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        form = FinanceExpenseForm(request.POST, request.FILES)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.requested_by = request.user
            expense.status = FinanceExpense.Status.REQUESTED
            expense.save()
            messages.success(request, f'Despesa {expense.title} enviada para analise.')
        else:
            for field_errors in form.errors.values():
                for error in field_errors:
                    messages.error(request, error)
        return redirect('finance-dashboard')


class FinanceExpenseDecisionView(FinanceOperatorRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        expense = get_object_or_404(FinanceExpense, pk=pk)
        form = FinanceExpenseDecisionForm(request.POST)
        if form.is_valid():
            decision = form.save(commit=False)
            decision.expense = expense
            decision.reviewer = request.user
            decision.save()
            if decision.decision == FinanceExpenseDecision.Decision.APPROVED:
                expense.status = FinanceExpense.Status.APPROVED
                expense.approved_by = request.user
            elif decision.decision == FinanceExpenseDecision.Decision.REJECTED:
                expense.status = FinanceExpense.Status.REJECTED
                expense.approved_by = request.user
            elif decision.decision == FinanceExpenseDecision.Decision.PAID:
                expense.status = FinanceExpense.Status.PAID
                expense.paid_by = request.user
                expense.payment_date = expense.payment_date or timezone.localdate()
            else:
                expense.status = FinanceExpense.Status.REVIEW
            expense.save(update_fields=['status', 'approved_by', 'paid_by', 'payment_date', 'updated_at'])
            messages.success(request, f'Decisao registrada para {expense.title}.')
        else:
            for field_errors in form.errors.values():
                for error in field_errors:
                    messages.error(request, error)
        return redirect('finance-dashboard')


class FinanceContributionCreateView(FinanceOperatorRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        form = FinanceContributionForm(request.POST)
        if form.is_valid():
            contribution = form.save(commit=False)
            contribution.recorded_by = request.user
            contribution.save()
            messages.success(request, f'Entrada financeira de {contribution.source_name} registrada.')
        else:
            for field_errors in form.errors.values():
                for error in field_errors:
                    messages.error(request, error)
        return redirect('finance-dashboard')


class FinanceCsvExportView(FinanceOperatorRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = 'attachment; filename="financeiro-prestacao-contas.csv"'
        writer = csv.writer(response, delimiter=';')
        writer.writerow(['tipo', 'data', 'categoria', 'descricao', 'valor', 'status', 'conta', 'responsavel', 'documento'])
        for contribution in FinanceContribution.objects.select_related('account', 'recorded_by'):
            writer.writerow(
                [
                    'entrada',
                    contribution.received_at,
                    contribution.get_source_type_display(),
                    contribution.source_name,
                    contribution.amount,
                    'recebido',
                    contribution.account.name if contribution.account else '',
                    contribution.recorded_by.display_name if contribution.recorded_by else '',
                    contribution.document_number,
                ]
            )
        for expense in FinanceExpense.objects.select_related('account', 'requested_by'):
            writer.writerow(
                [
                    'saida',
                    expense.expense_date,
                    expense.get_category_display(),
                    expense.title,
                    expense.amount,
                    expense.get_status_display(),
                    expense.account.name if expense.account else '',
                    expense.requested_by.display_name if expense.requested_by else '',
                    expense.document_number,
                ]
            )
        return response
