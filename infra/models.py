from django.conf import settings
from django.db import models
from django.utils import timezone


class InfraSector(models.TextChoices):
    TI = 'ti', 'TI'
    PRODUCTION = 'producao', 'Producao'
    GARDENING = 'jardinagem', 'Jardinagem'
    MAINTENANCE = 'manutencao', 'Manutencao'


INFRA_SECTOR_OPERATOR_FIELDS = {
    InfraSector.TI: 'is_infra_ti_operator',
    InfraSector.PRODUCTION: 'is_infra_production_operator',
    InfraSector.GARDENING: 'is_infra_gardening_operator',
    InfraSector.MAINTENANCE: 'is_infra_maintenance_operator',
}


class InfraRequest(models.Model):
    class Category(models.TextChoices):
        WIFI = 'wifi_rede', 'Wi-Fi / rede'
        COMPUTER = 'computador', 'Computador / maquina'
        FIELD = 'campo', 'Campo agricola'
        CROP = 'cultivo', 'Cultivo / ciclo produtivo'
        IRRIGATION = 'irrigacao', 'Irrigacao'
        GARDEN = 'jardim', 'Jardim / paisagismo'
        ELECTRICAL = 'eletrica', 'Eletrica'
        HYDRAULIC = 'hidraulica', 'Hidraulica'
        CONSTRUCTION = 'construcao', 'Construcao / estrutura'
        OTHER = 'outro', 'Outro'

    class Priority(models.TextChoices):
        LOW = 'baixa', 'Baixa'
        NORMAL = 'normal', 'Normal'
        HIGH = 'alta', 'Alta'
        URGENT = 'urgente', 'Urgente'

    class Status(models.TextChoices):
        NEW = 'nova', 'Nova'
        TRIAGE = 'triagem', 'Em triagem'
        SCHEDULED = 'agendada', 'Agendada'
        IN_PROGRESS = 'andamento', 'Em atendimento'
        WAITING = 'aguardando', 'Aguardando retorno'
        DONE = 'concluida', 'Concluida'
        CANCELLED = 'cancelada', 'Cancelada'

    requester = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='infra_requests',
    )
    sector = models.CharField(max_length=24, choices=InfraSector.choices, db_index=True)
    category = models.CharField(max_length=32, choices=Category.choices, default=Category.OTHER)
    title = models.CharField(max_length=160)
    location = models.CharField(max_length=160)
    asset_identifier = models.CharField(max_length=120, blank=True)
    description = models.TextField(max_length=2400)
    priority = models.CharField(max_length=16, choices=Priority.choices, default=Priority.NORMAL, db_index=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NEW, db_index=True)
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='assigned_infra_requests',
    )
    scheduled_for = models.DateTimeField(null=True, blank=True, db_index=True)
    closed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at', '-created_at']

    def __str__(self):
        return f'{self.get_sector_display()} - {self.title}'

    @property
    def is_open(self):
        return self.status not in {self.Status.DONE, self.Status.CANCELLED}

    def close_if_needed(self):
        if self.status in {self.Status.DONE, self.Status.CANCELLED} and self.closed_at is None:
            self.closed_at = timezone.now()
        if self.status not in {self.Status.DONE, self.Status.CANCELLED}:
            self.closed_at = None


class InfraRequestUpdate(models.Model):
    request = models.ForeignKey(InfraRequest, on_delete=models.CASCADE, related_name='updates')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='infra_request_updates',
    )
    body = models.TextField(max_length=1800)
    status_from = models.CharField(max_length=20, blank=True)
    status_to = models.CharField(max_length=20, blank=True)
    scheduled_for = models.DateTimeField(null=True, blank=True)
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'Atualizacao #{self.request_id} em {self.created_at:%d/%m/%Y %H:%M}'


class InfraCalendarEvent(models.Model):
    class Status(models.TextChoices):
        PLANNED = 'planejado', 'Planejado'
        CONFIRMED = 'confirmado', 'Confirmado'
        DONE = 'concluido', 'Concluido'
        CANCELLED = 'cancelado', 'Cancelado'

    sector = models.CharField(max_length=24, choices=InfraSector.choices, db_index=True)
    title = models.CharField(max_length=160)
    start_at = models.DateTimeField(db_index=True)
    end_at = models.DateTimeField(null=True, blank=True)
    location = models.CharField(max_length=160, blank=True)
    responsible = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='infra_calendar_responsibilities',
    )
    related_request = models.ForeignKey(
        InfraRequest,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='calendar_events',
    )
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PLANNED)
    notes = models.TextField(max_length=1200, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='created_infra_calendar_events',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['start_at', 'sector', 'title']

    def __str__(self):
        return f'{self.title} - {self.get_sector_display()}'


class TiInventoryItem(models.Model):
    class Kind(models.TextChoices):
        DESKTOP = 'desktop', 'Computador de mesa'
        NOTEBOOK = 'notebook', 'Notebook'
        SERVER = 'servidor', 'Servidor'
        ROUTER = 'roteador', 'Roteador'
        SWITCH = 'switch', 'Switch'
        ACCESS_POINT = 'access_point', 'Ponto de acesso'
        PRINTER = 'impressora', 'Impressora'
        PERIPHERAL = 'periferico', 'Periferico'
        OTHER = 'outro', 'Outro'

    class Status(models.TextChoices):
        ACTIVE = 'ativo', 'Ativo'
        MAINTENANCE = 'manutencao', 'Em manutencao'
        RESERVE = 'reserva', 'Reserva'
        RETIRED = 'baixado', 'Baixado'

    name = models.CharField(max_length=140)
    kind = models.CharField(max_length=24, choices=Kind.choices, default=Kind.DESKTOP, db_index=True)
    asset_code = models.CharField(max_length=80, blank=True, db_index=True)
    location = models.CharField(max_length=140)
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='assigned_ti_inventory_items',
    )
    ip_address = models.CharField(max_length=64, blank=True)
    mac_address = models.CharField(max_length=64, blank=True)
    operating_system = models.CharField(max_length=120, blank=True)
    status = models.CharField(max_length=24, choices=Status.choices, default=Status.ACTIVE, db_index=True)
    notes = models.TextField(max_length=1600, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='created_ti_inventory_items',
    )
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['kind', 'name']

    def __str__(self):
        return self.name

    @property
    def is_computer(self):
        return self.kind in {self.Kind.DESKTOP, self.Kind.NOTEBOOK, self.Kind.SERVER}


class TiNetworkNode(models.Model):
    class Kind(models.TextChoices):
        LINK = 'link', 'Link de internet'
        ROUTER = 'roteador', 'Roteador'
        SWITCH = 'switch', 'Switch'
        ACCESS_POINT = 'access_point', 'Ponto de acesso'
        SERVER = 'servidor', 'Servidor'
        SEGMENT = 'segmento', 'Segmento de rede'
        OTHER = 'outro', 'Outro'

    class Status(models.TextChoices):
        ACTIVE = 'ativo', 'Ativo'
        UNSTABLE = 'instavel', 'Instavel'
        MAINTENANCE = 'manutencao', 'Em manutencao'
        OFFLINE = 'desligado', 'Desligado'

    name = models.CharField(max_length=140)
    kind = models.CharField(max_length=24, choices=Kind.choices, default=Kind.ACCESS_POINT, db_index=True)
    location = models.CharField(max_length=140)
    ip_address = models.CharField(max_length=64, blank=True)
    ssid = models.CharField(max_length=120, blank=True)
    vlan = models.CharField(max_length=80, blank=True)
    upstream = models.CharField(max_length=140, blank=True)
    status = models.CharField(max_length=24, choices=Status.choices, default=Status.ACTIVE, db_index=True)
    notes = models.TextField(max_length=1600, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='created_ti_network_nodes',
    )
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['kind', 'name']

    def __str__(self):
        return self.name
