from decimal import Decimal

from django.conf import settings
from django.core.validators import FileExtensionValidator, MinValueValidator
from django.db import models
from django.utils import timezone

from core.security import build_protected_media_url


MONEY_VALIDATOR = MinValueValidator(Decimal('0.00'))


class FinanceAccount(models.Model):
    class Kind(models.TextChoices):
        CASH = 'caixa', 'Caixa fisico'
        BANK = 'banco', 'Conta bancaria'
        DIGITAL = 'digital', 'Conta digital'
        PROJECT = 'projeto', 'Fundo de projeto'
        OTHER = 'outro', 'Outro'

    name = models.CharField(max_length=140, unique=True)
    kind = models.CharField(max_length=20, choices=Kind.choices, default=Kind.CASH)
    holder_name = models.CharField(max_length=140, blank=True)
    reference_code = models.CharField(max_length=80, blank=True)
    opening_balance = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    is_active = models.BooleanField(default=True, db_index=True)
    notes = models.TextField(max_length=1200, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='created_finance_accounts',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class FinanceBudget(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'rascunho', 'Rascunho'
        SUBMITTED = 'enviado', 'Enviado para aprovacao'
        APPROVED = 'aprovado', 'Aprovado'
        REJECTED = 'recusado', 'Recusado'
        CLOSED = 'fechado', 'Fechado'

    title = models.CharField(max_length=160)
    period_start = models.DateField(default=timezone.localdate)
    period_end = models.DateField()
    description = models.TextField(max_length=2000, blank=True)
    total_planned = models.DecimalField(max_digits=12, decimal_places=2, validators=[MONEY_VALIDATOR])
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT, db_index=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='created_finance_budgets',
    )
    submitted_at = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='reviewed_finance_budgets',
    )
    reviewed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-period_start', '-created_at']

    def __str__(self):
        return self.title

    @property
    def is_open_for_expenses(self):
        return self.status == self.Status.APPROVED


class FinanceBudgetLine(models.Model):
    class Category(models.TextChoices):
        FOOD = 'alimentacao', 'Alimentacao'
        TRANSPORT = 'transporte', 'Transporte'
        EDUCATION = 'formacao', 'Formacao'
        COMMUNICATION = 'comunicacao', 'Comunicacao'
        INFRA = 'infraestrutura', 'Infraestrutura'
        HEALTH = 'saude', 'Saude'
        PRODUCTION = 'producao', 'Producao'
        SOLIDARITY = 'solidariedade', 'Solidariedade'
        ADMIN = 'administrativo', 'Administrativo'
        OTHER = 'outro', 'Outro'

    budget = models.ForeignKey(FinanceBudget, on_delete=models.CASCADE, related_name='lines')
    category = models.CharField(max_length=24, choices=Category.choices, default=Category.OTHER)
    description = models.CharField(max_length=180)
    planned_amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MONEY_VALIDATOR])
    notes = models.TextField(max_length=1000, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['category', 'description']

    def __str__(self):
        return f'{self.budget} - {self.get_category_display()}'


class FinanceBudgetReview(models.Model):
    class Decision(models.TextChoices):
        APPROVED = 'aprovado', 'Aprovado'
        REJECTED = 'recusado', 'Recusado'
        REVISION = 'revisao', 'Pedir revisao'

    budget = models.ForeignKey(FinanceBudget, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='finance_budget_reviews',
    )
    decision = models.CharField(max_length=20, choices=Decision.choices)
    note = models.TextField(max_length=1200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.budget} - {self.get_decision_display()}'


class FinanceExpense(models.Model):
    class Status(models.TextChoices):
        REQUESTED = 'solicitado', 'Solicitado'
        REVIEW = 'analise', 'Em analise'
        APPROVED = 'aprovado', 'Aprovado'
        PAID = 'pago', 'Pago'
        REJECTED = 'recusado', 'Recusado'
        CANCELLED = 'cancelado', 'Cancelado'

    class PaymentMethod(models.TextChoices):
        CASH = 'dinheiro', 'Dinheiro'
        PIX = 'pix', 'PIX'
        CARD = 'cartao', 'Cartao'
        TRANSFER = 'transferencia', 'Transferencia'
        BOLETO = 'boleto', 'Boleto'
        OTHER = 'outro', 'Outro'

    budget = models.ForeignKey(
        FinanceBudget,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='expenses',
    )
    account = models.ForeignKey(
        FinanceAccount,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='expenses',
    )
    category = models.CharField(max_length=24, choices=FinanceBudgetLine.Category.choices, default=FinanceBudgetLine.Category.OTHER)
    title = models.CharField(max_length=160)
    supplier = models.CharField(max_length=160, blank=True)
    document_number = models.CharField(max_length=80, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MONEY_VALIDATOR])
    expense_date = models.DateField(default=timezone.localdate)
    due_date = models.DateField(null=True, blank=True)
    payment_date = models.DateField(null=True, blank=True)
    payment_method = models.CharField(max_length=20, choices=PaymentMethod.choices, default=PaymentMethod.PIX)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.REQUESTED, db_index=True)
    requested_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='requested_finance_expenses',
    )
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='approved_finance_expenses',
    )
    paid_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='paid_finance_expenses',
    )
    receipt = models.FileField(
        upload_to='financeiro/comprovantes/%Y/%m/',
        blank=True,
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp', 'pdf'])],
    )
    justification = models.TextField(max_length=1800)
    notes = models.TextField(max_length=1200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-expense_date', '-created_at']

    def __str__(self):
        return f'{self.title} - R$ {self.amount}'

    @property
    def receipt_view_url(self):
        if not self.receipt:
            return ''
        return build_protected_media_url('finance-expense-receipt', self.pk, action='view')

    @property
    def receipt_download_url(self):
        if not self.receipt:
            return ''
        return build_protected_media_url('finance-expense-receipt', self.pk, action='download')


class FinanceExpenseDecision(models.Model):
    class Decision(models.TextChoices):
        APPROVED = 'aprovado', 'Aprovado'
        REJECTED = 'recusado', 'Recusado'
        REVISION = 'revisao', 'Pedir ajuste'
        PAID = 'pago', 'Marcado como pago'

    expense = models.ForeignKey(FinanceExpense, on_delete=models.CASCADE, related_name='decisions')
    reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='finance_expense_decisions',
    )
    decision = models.CharField(max_length=20, choices=Decision.choices)
    note = models.TextField(max_length=1200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.expense} - {self.get_decision_display()}'


class FinanceContribution(models.Model):
    class SourceType(models.TextChoices):
        MEMBER = 'militante', 'Militante'
        DONATION = 'doacao', 'Doacao'
        EVENT = 'evento', 'Evento'
        GRANT = 'parceria', 'Parceria/projeto'
        SALE = 'venda', 'Venda solidaria'
        OTHER = 'outro', 'Outro'

    account = models.ForeignKey(
        FinanceAccount,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='contributions',
    )
    source_type = models.CharField(max_length=20, choices=SourceType.choices, default=SourceType.DONATION)
    source_name = models.CharField(max_length=160)
    amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MONEY_VALIDATOR])
    received_at = models.DateField(default=timezone.localdate)
    document_number = models.CharField(max_length=80, blank=True)
    notes = models.TextField(max_length=1200, blank=True)
    recorded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='recorded_finance_contributions',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-received_at', '-created_at']

    def __str__(self):
        return f'{self.source_name} - R$ {self.amount}'
