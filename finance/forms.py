from django import forms

from core.security import clean_plain_text

from .models import (
    FinanceAccount,
    FinanceBudget,
    FinanceBudgetLine,
    FinanceBudgetReview,
    FinanceContribution,
    FinanceExpense,
    FinanceExpenseDecision,
)


class FinanceAccountForm(forms.ModelForm):
    class Meta:
        model = FinanceAccount
        fields = ('name', 'kind', 'holder_name', 'reference_code', 'opening_balance', 'notes')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = 'Nome da conta/caixa'
        self.fields['kind'].label = 'Tipo'
        self.fields['holder_name'].label = 'Titular/responsavel'
        self.fields['reference_code'].label = 'Referencia interna'
        self.fields['opening_balance'].label = 'Saldo inicial'
        self.fields['notes'].label = 'Observacoes'

    def clean_name(self):
        return clean_plain_text(self.cleaned_data['name'])

    def clean_holder_name(self):
        return clean_plain_text(self.cleaned_data.get('holder_name', ''))

    def clean_reference_code(self):
        return clean_plain_text(self.cleaned_data.get('reference_code', ''))

    def clean_notes(self):
        return clean_plain_text(self.cleaned_data.get('notes', ''))


class FinanceBudgetForm(forms.ModelForm):
    class Meta:
        model = FinanceBudget
        fields = ('title', 'period_start', 'period_end', 'total_planned', 'description')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].label = 'Nome do orcamento'
        self.fields['period_start'].label = 'Inicio'
        self.fields['period_start'].widget.attrs.update({'type': 'date'})
        self.fields['period_end'].label = 'Fim'
        self.fields['period_end'].widget.attrs.update({'type': 'date'})
        self.fields['total_planned'].label = 'Valor planejado'
        self.fields['description'].label = 'Objetivo do orcamento'

    def clean_title(self):
        return clean_plain_text(self.cleaned_data['title'])

    def clean_description(self):
        return clean_plain_text(self.cleaned_data.get('description', ''))

    def clean(self):
        cleaned = super().clean()
        start = cleaned.get('period_start')
        end = cleaned.get('period_end')
        if start and end and end < start:
            self.add_error('period_end', 'A data final precisa ser depois do inicio.')
        return cleaned


class FinanceBudgetLineForm(forms.ModelForm):
    class Meta:
        model = FinanceBudgetLine
        fields = ('budget', 'category', 'description', 'planned_amount', 'notes')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['budget'].label = 'Orcamento'
        self.fields['budget'].queryset = FinanceBudget.objects.exclude(status=FinanceBudget.Status.CLOSED)
        self.fields['category'].label = 'Categoria'
        self.fields['description'].label = 'Linha/atividade'
        self.fields['planned_amount'].label = 'Valor previsto'
        self.fields['notes'].label = 'Observacoes'

    def clean_description(self):
        return clean_plain_text(self.cleaned_data['description'])

    def clean_notes(self):
        return clean_plain_text(self.cleaned_data.get('notes', ''))


class FinanceContributionForm(forms.ModelForm):
    class Meta:
        model = FinanceContribution
        fields = ('account', 'source_type', 'source_name', 'amount', 'received_at', 'document_number', 'notes')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['account'].label = 'Conta/caixa de entrada'
        self.fields['account'].queryset = FinanceAccount.objects.filter(is_active=True)
        self.fields['source_type'].label = 'Origem'
        self.fields['source_name'].label = 'Fonte/descricao'
        self.fields['amount'].label = 'Valor'
        self.fields['received_at'].label = 'Data de recebimento'
        self.fields['received_at'].widget.attrs.update({'type': 'date'})
        self.fields['document_number'].label = 'Documento/recibo'
        self.fields['notes'].label = 'Observacoes'

    def clean_source_name(self):
        return clean_plain_text(self.cleaned_data['source_name'])

    def clean_document_number(self):
        return clean_plain_text(self.cleaned_data.get('document_number', ''))

    def clean_notes(self):
        return clean_plain_text(self.cleaned_data.get('notes', ''))


class FinanceExpenseForm(forms.ModelForm):
    class Meta:
        model = FinanceExpense
        fields = (
            'budget',
            'account',
            'category',
            'title',
            'supplier',
            'document_number',
            'amount',
            'expense_date',
            'due_date',
            'payment_method',
            'receipt',
            'justification',
            'notes',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['budget'].label = 'Orcamento vinculado'
        self.fields['budget'].required = False
        self.fields['budget'].queryset = FinanceBudget.objects.filter(status=FinanceBudget.Status.APPROVED)
        self.fields['account'].label = 'Conta/caixa previsto'
        self.fields['account'].required = False
        self.fields['account'].queryset = FinanceAccount.objects.filter(is_active=True)
        self.fields['category'].label = 'Categoria'
        self.fields['title'].label = 'Despesa'
        self.fields['supplier'].label = 'Fornecedor/pessoa'
        self.fields['document_number'].label = 'Nota/recibo/documento'
        self.fields['amount'].label = 'Valor'
        self.fields['expense_date'].label = 'Data da despesa'
        self.fields['expense_date'].widget.attrs.update({'type': 'date'})
        self.fields['due_date'].label = 'Vencimento'
        self.fields['due_date'].required = False
        self.fields['due_date'].widget.attrs.update({'type': 'date'})
        self.fields['payment_method'].label = 'Forma de pagamento'
        self.fields['receipt'].label = 'Comprovante'
        self.fields['justification'].label = 'Justificativa'
        self.fields['notes'].label = 'Observacoes'

    def clean_title(self):
        return clean_plain_text(self.cleaned_data['title'])

    def clean_supplier(self):
        return clean_plain_text(self.cleaned_data.get('supplier', ''))

    def clean_document_number(self):
        return clean_plain_text(self.cleaned_data.get('document_number', ''))

    def clean_justification(self):
        return clean_plain_text(self.cleaned_data['justification'])

    def clean_notes(self):
        return clean_plain_text(self.cleaned_data.get('notes', ''))


class FinanceBudgetReviewForm(forms.ModelForm):
    class Meta:
        model = FinanceBudgetReview
        fields = ('decision', 'note')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['decision'].label = 'Decisao'
        self.fields['note'].label = 'Parecer'

    def clean_note(self):
        return clean_plain_text(self.cleaned_data.get('note', ''))


class FinanceExpenseDecisionForm(forms.ModelForm):
    class Meta:
        model = FinanceExpenseDecision
        fields = ('decision', 'note')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['decision'].label = 'Decisao'
        self.fields['note'].label = 'Parecer'

    def clean_note(self):
        return clean_plain_text(self.cleaned_data.get('note', ''))
