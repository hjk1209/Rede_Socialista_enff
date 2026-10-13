from django.urls import path

from .views import (
    FinanceAccountCreateView,
    FinanceBudgetCreateView,
    FinanceBudgetLineCreateView,
    FinanceBudgetReviewView,
    FinanceBudgetSubmitView,
    FinanceContributionCreateView,
    FinanceCsvExportView,
    FinanceDashboardView,
    FinanceExpenseCreateView,
    FinanceExpenseDecisionView,
)


urlpatterns = [
    path('', FinanceDashboardView.as_view(), name='finance-dashboard'),
    path('contas/criar/', FinanceAccountCreateView.as_view(), name='finance-account-create'),
    path('orcamentos/criar/', FinanceBudgetCreateView.as_view(), name='finance-budget-create'),
    path('orcamentos/linhas/criar/', FinanceBudgetLineCreateView.as_view(), name='finance-budget-line-create'),
    path('orcamentos/<int:pk>/enviar/', FinanceBudgetSubmitView.as_view(), name='finance-budget-submit'),
    path('orcamentos/<int:pk>/parecer/', FinanceBudgetReviewView.as_view(), name='finance-budget-review'),
    path('despesas/criar/', FinanceExpenseCreateView.as_view(), name='finance-expense-create'),
    path('despesas/<int:pk>/decidir/', FinanceExpenseDecisionView.as_view(), name='finance-expense-decision'),
    path('entradas/criar/', FinanceContributionCreateView.as_view(), name='finance-contribution-create'),
    path('exportar/prestacao-contas.csv/', FinanceCsvExportView.as_view(), name='finance-export-csv'),
]
