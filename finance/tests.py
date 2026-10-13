from decimal import Decimal

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from accounts.models import User

from .models import (
    FinanceAccount,
    FinanceBudget,
    FinanceBudgetLine,
    FinanceBudgetReview,
    FinanceContribution,
    FinanceExpense,
    FinanceExpenseDecision,
)


class FinanceAccessTests(TestCase):
    password = 'SenhaSegura!2026'

    def create_user(self, username, **extra_fields):
        return User.objects.create_user(
            username=username,
            display_name=extra_fields.pop('display_name', username.title()),
            handle=extra_fields.pop('handle', username.replace('.', '_')),
            email=extra_fields.pop('email', f'{username}@example.com'),
            password=self.password,
            **extra_fields,
        )

    def test_member_without_finance_permission_is_redirected(self):
        user = self.create_user('membro')
        self.client.force_login(user)

        response = self.client.get(reverse('finance-dashboard'))

        self.assertRedirects(response, reverse('feed'))

    def test_finance_operator_can_open_dashboard(self):
        operator = self.create_user('financeiro', is_finance_operator=True)
        self.client.force_login(operator)

        response = self.client.get(reverse('finance-dashboard'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Gestao financeira do movimento')
        self.assertContains(response, 'Exportar prestacao de contas')
        self.assertNotContains(response, '>Infra</a>', html=False)
        self.assertNotContains(response, '<span>Infra</span>', html=False)

    def test_finance_dashboard_uses_tabbed_card_model(self):
        operator = self.create_user('financeiro.tabs', is_finance_operator=True)
        self.client.force_login(operator)

        response = self.client.get(reverse('finance-dashboard'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'finance-tab-budgets')
        self.assertContains(response, 'finance-tab-expenses')
        self.assertContains(response, 'finance-tab-income')
        self.assertContains(response, 'finance-tab-accounts')
        self.assertContains(response, 'finance-tab-accountability')
        self.assertContains(response, 'Fluxo de trabalho')
        self.assertContains(response, 'Gasto com comprovante')
        self.assertContains(response, 'data-finance-tabs')
        self.assertContains(response, 'openFinanceTab')


class FinanceWorkflowTests(TestCase):
    password = 'SenhaSegura!2026'

    def setUp(self):
        self.operator = User.objects.create_user(
            username='financeiro',
            display_name='Coordenacao Financeira',
            handle='financeiro',
            email='financeiro@example.com',
            password=self.password,
            is_finance_operator=True,
        )
        self.client.force_login(self.operator)
        self.today = timezone.localdate()

    def test_budget_can_be_created_submitted_and_approved(self):
        response = self.client.post(
            reverse('finance-budget-create'),
            {
                'title': 'Jornada de formacao',
                'period_start': self.today.isoformat(),
                'period_end': self.today.replace(day=28).isoformat(),
                'total_planned': '2500.00',
                'description': 'Custeio coletivo da jornada.',
            },
        )

        self.assertRedirects(response, reverse('finance-dashboard'))
        budget = FinanceBudget.objects.get(title='Jornada de formacao')
        self.assertEqual(budget.created_by, self.operator)
        self.assertEqual(budget.status, FinanceBudget.Status.DRAFT)

        response = self.client.post(
            reverse('finance-budget-line-create'),
            {
                'budget': budget.pk,
                'category': FinanceBudgetLine.Category.FOOD,
                'description': 'Alimentacao coletiva',
                'planned_amount': '1200.00',
                'notes': 'Cafe, almoco e janta.',
            },
        )

        self.assertRedirects(response, reverse('finance-dashboard'))
        self.assertEqual(budget.lines.count(), 1)

        response = self.client.post(reverse('finance-budget-submit', args=[budget.pk]))
        self.assertRedirects(response, reverse('finance-dashboard'))
        budget.refresh_from_db()
        self.assertEqual(budget.status, FinanceBudget.Status.SUBMITTED)
        self.assertIsNotNone(budget.submitted_at)

        response = self.client.post(
            reverse('finance-budget-review', args=[budget.pk]),
            {'decision': FinanceBudgetReview.Decision.APPROVED, 'note': 'Aprovado pela coordenacao.'},
        )

        self.assertRedirects(response, reverse('finance-dashboard'))
        budget.refresh_from_db()
        self.assertEqual(budget.status, FinanceBudget.Status.APPROVED)
        self.assertEqual(budget.reviewed_by, self.operator)
        self.assertEqual(budget.reviews.count(), 1)

    def test_contribution_expense_approval_payment_and_csv_export(self):
        account = FinanceAccount.objects.create(
            name='Caixa geral',
            kind=FinanceAccount.Kind.CASH,
            opening_balance=Decimal('100.00'),
            created_by=self.operator,
        )
        budget = FinanceBudget.objects.create(
            title='Mutirao agricola',
            period_start=self.today,
            period_end=self.today.replace(day=28),
            total_planned=Decimal('900.00'),
            status=FinanceBudget.Status.APPROVED,
            created_by=self.operator,
        )

        response = self.client.post(
            reverse('finance-contribution-create'),
            {
                'account': account.pk,
                'source_type': FinanceContribution.SourceType.MEMBER,
                'source_name': 'Contribuicao solidaria',
                'amount': '300.00',
                'received_at': self.today.isoformat(),
                'document_number': 'REC-001',
                'notes': 'Entrada para mutirao.',
            },
        )
        self.assertRedirects(response, reverse('finance-dashboard'))
        contribution = FinanceContribution.objects.get(source_name='Contribuicao solidaria')
        self.assertEqual(contribution.recorded_by, self.operator)

        response = self.client.post(
            reverse('finance-expense-create'),
            {
                'budget': budget.pk,
                'account': account.pk,
                'category': FinanceBudgetLine.Category.FOOD,
                'title': 'Compra de alimentos',
                'supplier': 'Mercado local',
                'document_number': 'NF-001',
                'amount': '180.00',
                'expense_date': self.today.isoformat(),
                'due_date': '',
                'payment_method': FinanceExpense.PaymentMethod.PIX,
                'justification': 'Alimentacao do mutirao.',
                'notes': '',
            },
        )
        self.assertRedirects(response, reverse('finance-dashboard'))
        expense = FinanceExpense.objects.get(title='Compra de alimentos')
        self.assertEqual(expense.requested_by, self.operator)
        self.assertEqual(expense.status, FinanceExpense.Status.REQUESTED)

        response = self.client.post(
            reverse('finance-expense-decision', args=[expense.pk]),
            {'decision': FinanceExpenseDecision.Decision.APPROVED, 'note': 'Despesa dentro do orcamento.'},
        )
        self.assertRedirects(response, reverse('finance-dashboard'))
        expense.refresh_from_db()
        self.assertEqual(expense.status, FinanceExpense.Status.APPROVED)
        self.assertEqual(expense.approved_by, self.operator)

        response = self.client.post(
            reverse('finance-expense-decision', args=[expense.pk]),
            {'decision': FinanceExpenseDecision.Decision.PAID, 'note': 'Pago por PIX.'},
        )
        self.assertRedirects(response, reverse('finance-dashboard'))
        expense.refresh_from_db()
        self.assertEqual(expense.status, FinanceExpense.Status.PAID)
        self.assertEqual(expense.paid_by, self.operator)
        self.assertEqual(expense.payment_date, self.today)

        response = self.client.get(reverse('finance-export-csv'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('text/csv', response['Content-Type'])
        content = response.content.decode('utf-8')
        self.assertIn('entrada;', content)
        self.assertIn('saida;', content)
        self.assertIn('Compra de alimentos', content)
