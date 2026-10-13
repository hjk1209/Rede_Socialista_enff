from django.contrib import admin

from .models import (
    FinanceAccount,
    FinanceBudget,
    FinanceBudgetLine,
    FinanceBudgetReview,
    FinanceContribution,
    FinanceExpense,
    FinanceExpenseDecision,
)


class FinanceBudgetLineInline(admin.TabularInline):
    model = FinanceBudgetLine
    extra = 0


class FinanceBudgetReviewInline(admin.TabularInline):
    model = FinanceBudgetReview
    extra = 0
    readonly_fields = ('created_at',)


@admin.register(FinanceAccount)
class FinanceAccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'kind', 'opening_balance', 'is_active', 'created_at')
    list_filter = ('kind', 'is_active')
    search_fields = ('name', 'holder_name', 'reference_code')


@admin.register(FinanceBudget)
class FinanceBudgetAdmin(admin.ModelAdmin):
    list_display = ('title', 'period_start', 'period_end', 'total_planned', 'status', 'created_by')
    list_filter = ('status', 'period_start')
    search_fields = ('title', 'description')
    inlines = [FinanceBudgetLineInline, FinanceBudgetReviewInline]


class FinanceExpenseDecisionInline(admin.TabularInline):
    model = FinanceExpenseDecision
    extra = 0
    readonly_fields = ('created_at',)


@admin.register(FinanceExpense)
class FinanceExpenseAdmin(admin.ModelAdmin):
    list_display = ('title', 'amount', 'category', 'status', 'expense_date', 'requested_by', 'approved_by', 'paid_by')
    list_filter = ('status', 'category', 'payment_method', 'expense_date')
    search_fields = ('title', 'supplier', 'document_number', 'justification')
    inlines = [FinanceExpenseDecisionInline]


@admin.register(FinanceContribution)
class FinanceContributionAdmin(admin.ModelAdmin):
    list_display = ('source_name', 'source_type', 'amount', 'received_at', 'account', 'recorded_by')
    list_filter = ('source_type', 'received_at')
    search_fields = ('source_name', 'document_number', 'notes')


admin.site.register(FinanceBudgetLine)
admin.site.register(FinanceBudgetReview)
admin.site.register(FinanceExpenseDecision)
