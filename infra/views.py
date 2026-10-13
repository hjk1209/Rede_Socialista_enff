from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.views import View
from django.views.generic import TemplateView

from .forms import (
    InfraCalendarEventForm,
    InfraRequestForm,
    InfraRequestManageForm,
    InfraRequestUpdateForm,
    TiInventoryItemForm,
    TiNetworkNodeForm,
    TiSupportRequestForm,
)
from .models import (
    INFRA_SECTOR_OPERATOR_FIELDS,
    InfraCalendarEvent,
    InfraRequest,
    InfraRequestUpdate,
    InfraSector,
    TiInventoryItem,
    TiNetworkNode,
)


SECTOR_DESCRIPTIONS = {
    InfraSector.TI: 'Rede Wi-Fi, computadores, maquinas em uso, suporte tecnico e canal direto com usuarios.',
    InfraSector.PRODUCTION: 'Planejamento, acompanhamento e gestao do ciclo de producao agricola da escola.',
    InfraSector.GARDENING: 'Organizacao, cuidado e gestao de jardins, areas verdes e paisagismo da escola.',
    InfraSector.MAINTENANCE: 'Demandas hidraulicas, eletricas, estruturais e manutencoes gerais da escola.',
}

SECTOR_FOCUS_CARDS = {
    InfraSector.TI: [
        {
            'kicker': 'Conectividade',
            'title': 'Rede Wi-Fi e internet',
            'body': 'Mapear quedas, pontos sem sinal, roteadores, senhas, salas conectadas e prioridades de atendimento.',
        },
        {
            'kicker': 'Equipamentos',
            'title': 'Computadores e maquinas',
            'body': 'Registrar computador, local, operador, problema, historico de reparo e agenda de manutencao.',
        },
        {
            'kicker': 'Dialogo',
            'title': 'Canal direto com usuarios',
            'body': 'Manter conversa aberta com solicitantes, orientar uso e avisar agendamentos ou conclusoes.',
        },
    ],
    InfraSector.PRODUCTION: [
        {
            'kicker': 'Planejamento',
            'title': 'Ciclo agricola',
            'body': 'Organizar plantio, manejo, colheita, insumos, equipes, areas produtivas e datas de acompanhamento.',
        },
        {
            'kicker': 'Campo',
            'title': 'Atividades de producao',
            'body': 'Registrar demandas de irrigacao, cultivo, canteiros, ferramentas e necessidades do trabalho de campo.',
        },
        {
            'kicker': 'Gestao',
            'title': 'Acompanhamento produtivo',
            'body': 'Conectar solicitacoes, calendario comum e responsaveis para evitar perda de etapa no ciclo.',
        },
    ],
    InfraSector.GARDENING: [
        {
            'kicker': 'Cuidado',
            'title': 'Jardins e areas verdes',
            'body': 'Controlar poda, limpeza, irrigacao, ornamentacao, mudas e prioridades de cuidado dos espacos.',
        },
        {
            'kicker': 'Organizacao',
            'title': 'Paisagismo da escola',
            'body': 'Planejar melhorias visuais, rotas de cuidado, materiais necessarios e acompanhamento das areas externas.',
        },
        {
            'kicker': 'Agenda',
            'title': 'Rotina de jardinagem',
            'body': 'Agendar mutiroes, manutencoes periodicas e comunicados para quem usa ou cuida dos espacos.',
        },
    ],
    InfraSector.MAINTENANCE: [
        {
            'kicker': 'Predial',
            'title': 'Hidraulica e eletrica',
            'body': 'Priorizar vazamentos, registros, tomadas, iluminacao, quadros eletricos e riscos operacionais.',
        },
        {
            'kicker': 'Estrutura',
            'title': 'Construcao e reparos',
            'body': 'Acompanhar portas, telhados, paredes, pisos, mobiliario, salas e estruturas comuns da escola.',
        },
        {
            'kicker': 'Execucao',
            'title': 'Manutencao geral',
            'body': 'Transformar solicitacoes em agenda, responsavel, status e historico de conclusao.',
        },
    ],
}


def is_infra_coordinator(user):
    return bool(
        getattr(user, 'is_authenticated', False)
        and (
            getattr(user, 'is_infra_coordinator', False)
            or getattr(user, 'can_administer', False)
            or getattr(user, 'can_found', False)
            or getattr(user, 'is_superuser', False)
        )
    )


def managed_sector_codes(user):
    if is_infra_coordinator(user):
        return [code for code, _ in InfraSector.choices]
    if not getattr(user, 'is_authenticated', False):
        return []
    return [
        code
        for code, field_name in INFRA_SECTOR_OPERATOR_FIELDS.items()
        if getattr(user, field_name, False)
    ]


def can_manage_sector(user, sector):
    return sector in managed_sector_codes(user)


def can_access_infra_operations(user):
    return bool(managed_sector_codes(user))


def visible_requests_for(user):
    requests = InfraRequest.objects.select_related('requester', 'assigned_to').prefetch_related('updates__author')
    if is_infra_coordinator(user):
        return requests
    sectors = managed_sector_codes(user)
    query = Q(requester=user)
    if sectors:
        query |= Q(sector__in=sectors)
    return requests.filter(query).distinct()


def can_view_request(user, infra_request):
    return visible_requests_for(user).filter(pk=infra_request.pk).exists()


def can_manage_request(user, infra_request):
    return can_manage_sector(user, infra_request.sector)


class InfraDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'infra/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.localdate()
        month_start = today.replace(day=1)
        visible_requests = visible_requests_for(self.request.user)
        managed_sectors = managed_sector_codes(self.request.user)
        is_operator = bool(managed_sectors)
        ti_ticket_queryset = visible_requests.filter(sector=InfraSector.TI)
        ti_computer_kinds = [
            TiInventoryItem.Kind.DESKTOP,
            TiInventoryItem.Kind.NOTEBOOK,
            TiInventoryItem.Kind.SERVER,
        ]
        calendar_events = InfraCalendarEvent.objects.select_related(
            'responsible',
            'related_request',
            'created_by',
        ).filter(start_at__date__gte=month_start)

        context['request_form'] = kwargs.get('request_form') or InfraRequestForm()
        context['calendar_form'] = kwargs.get('calendar_form') or InfraCalendarEventForm(
            allowed_sectors=managed_sectors if is_operator else [],
            initial={'responsible': self.request.user},
        )
        context['managed_sectors'] = managed_sectors
        context['is_infra_operator'] = is_operator
        context['is_infra_coordinator'] = is_infra_coordinator(self.request.user)
        context['can_manage_ti'] = can_manage_sector(self.request.user, InfraSector.TI)
        context['ti_ticket_form'] = kwargs.get('ti_ticket_form') or TiSupportRequestForm()
        context['ti_inventory_form'] = kwargs.get('ti_inventory_form') or TiInventoryItemForm()
        context['ti_network_form'] = kwargs.get('ti_network_form') or TiNetworkNodeForm()
        context['ti_inventory_items'] = TiInventoryItem.objects.select_related('assigned_to')[:20]
        context['ti_computers'] = TiInventoryItem.objects.select_related('assigned_to').filter(
            kind__in=ti_computer_kinds
        )[:12]
        context['ti_network_nodes'] = TiNetworkNode.objects.select_related('created_by')[:20]
        context['ti_ticket_cards'] = ti_ticket_queryset[:8]
        context['sector_cards'] = [
            {
                'code': code,
                'label': label,
                'description': SECTOR_DESCRIPTIONS.get(code, ''),
                'focus_cards': SECTOR_FOCUS_CARDS.get(code, []),
                'can_manage': code in managed_sectors,
                'open_total': InfraRequest.objects.filter(sector=code).exclude(
                    status__in=[InfraRequest.Status.DONE, InfraRequest.Status.CANCELLED]
                ).count(),
                'scheduled_total': InfraRequest.objects.filter(sector=code, scheduled_for__isnull=False).exclude(
                    status__in=[InfraRequest.Status.DONE, InfraRequest.Status.CANCELLED]
                ).count(),
                'month_event_total': calendar_events.filter(sector=code).count(),
                'visible_requests': visible_requests.filter(sector=code)[:3],
                'events': calendar_events.filter(sector=code)[:3],
            }
            for code, label in InfraSector.choices
        ]
        requests = visible_requests[:20]
        context['request_cards'] = [
            {
                'instance': request_item,
                'can_manage': can_manage_request(self.request.user, request_item),
                'update_form': InfraRequestUpdateForm(),
                'manage_form': InfraRequestManageForm(instance=request_item),
            }
            for request_item in requests
        ]
        context['calendar_events'] = calendar_events[:18]
        context['my_notifications'] = InfraRequestUpdate.objects.filter(
            Q(request__requester=self.request.user)
            | Q(request__assigned_to=self.request.user)
            | Q(request__sector__in=managed_sectors)
        ).select_related('request', 'author').exclude(author=self.request.user)[:12]
        context['open_request_total'] = visible_requests.exclude(
            status__in=[InfraRequest.Status.DONE, InfraRequest.Status.CANCELLED]
        ).count()
        context['scheduled_request_total'] = visible_requests.filter(scheduled_for__isnull=False).exclude(
            status__in=[InfraRequest.Status.DONE, InfraRequest.Status.CANCELLED]
        ).count()
        context['month_event_total'] = InfraCalendarEvent.objects.filter(start_at__date__gte=month_start).count()
        return context


class InfraRequestCreateView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        form = InfraRequestForm(request.POST)
        if form.is_valid():
            infra_request = form.save(commit=False)
            infra_request.requester = request.user
            infra_request.save()
            InfraRequestUpdate.objects.create(
                request=infra_request,
                author=request.user,
                body='Solicitacao aberta para o setor de infra.',
                status_to=infra_request.status,
            )
            messages.success(request, 'Solicitacao enviada para o setor de infra.')
        else:
            for field_errors in form.errors.values():
                for error in field_errors:
                    messages.error(request, error)
        return redirect('infra-dashboard')


class InfraRequestUpdateCreateView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        infra_request = get_object_or_404(InfraRequest, pk=pk)
        if not can_view_request(request.user, infra_request):
            messages.error(request, 'Essa solicitacao nao esta disponivel para seu perfil.')
            return redirect('infra-dashboard')
        form = InfraRequestUpdateForm(request.POST)
        if form.is_valid():
            InfraRequestUpdate.objects.create(
                request=infra_request,
                author=request.user,
                body=form.cleaned_data['body'],
                status_to=infra_request.status,
                scheduled_for=infra_request.scheduled_for,
            )
            messages.success(request, 'Mensagem registrada na solicitacao.')
        else:
            for field_errors in form.errors.values():
                for error in field_errors:
                    messages.error(request, error)
        return redirect('infra-dashboard')


class InfraRequestManageView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        infra_request = get_object_or_404(InfraRequest, pk=pk)
        if not can_manage_request(request.user, infra_request):
            messages.error(request, 'Seu perfil nao gerencia este setor da infra.')
            return redirect('infra-dashboard')

        previous_status = infra_request.status
        previous_schedule = infra_request.scheduled_for
        form = InfraRequestManageForm(request.POST, instance=infra_request)
        if form.is_valid():
            updated_request = form.save(commit=False)
            updated_request.close_if_needed()
            updated_request.save()
            form.save_m2m()
            body_parts = ['Solicitacao atualizada pela infra.']
            if previous_status != updated_request.status:
                body_parts.append(f'Status: {updated_request.get_status_display()}.')
            if previous_schedule != updated_request.scheduled_for and updated_request.scheduled_for:
                body_parts.append(f'Agendamento: {updated_request.scheduled_for:%d/%m/%Y %H:%M}.')
            InfraRequestUpdate.objects.create(
                request=updated_request,
                author=request.user,
                body=' '.join(body_parts),
                status_from=previous_status,
                status_to=updated_request.status,
                scheduled_for=updated_request.scheduled_for,
            )
            messages.success(request, 'Solicitacao de infra atualizada.')
        else:
            for field_errors in form.errors.values():
                for error in field_errors:
                    messages.error(request, error)
        return redirect('infra-dashboard')


class InfraCalendarEventCreateView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        managed_sectors = managed_sector_codes(request.user)
        if not managed_sectors:
            messages.error(request, 'Apenas operadores de infra podem criar agenda de setor.')
            return redirect('infra-dashboard')
        form = InfraCalendarEventForm(request.POST, allowed_sectors=managed_sectors)
        if form.is_valid():
            event = form.save(commit=False)
            if not can_manage_sector(request.user, event.sector):
                messages.error(request, 'Seu perfil nao gerencia este setor da infra.')
                return redirect('infra-dashboard')
            event.created_by = request.user
            if not event.responsible:
                event.responsible = request.user
            event.save()
            messages.success(request, 'Atividade adicionada ao calendario comum da infra.')
        else:
            for field_errors in form.errors.values():
                for error in field_errors:
                    messages.error(request, error)
        return redirect('infra-dashboard')


class TiSupportRequestCreateView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        form = TiSupportRequestForm(request.POST)
        if form.is_valid():
            infra_request = form.save(commit=False)
            infra_request.requester = request.user
            infra_request.sector = InfraSector.TI
            infra_request.save()
            InfraRequestUpdate.objects.create(
                request=infra_request,
                author=request.user,
                body='Chamado direto de TI aberto pelo usuario.',
                status_to=infra_request.status,
            )
            messages.success(request, 'Chamado enviado diretamente para a TI.')
        else:
            for field_errors in form.errors.values():
                for error in field_errors:
                    messages.error(request, error)
        return redirect('infra-dashboard')


class TiInventoryItemCreateView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        if not can_manage_sector(request.user, InfraSector.TI):
            messages.error(request, 'Apenas a TI ou coordenacao da infra pode gerenciar inventario.')
            return redirect('infra-dashboard')

        form = TiInventoryItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.created_by = request.user
            item.save()
            messages.success(request, 'Item de inventario da TI cadastrado.')
        else:
            for field_errors in form.errors.values():
                for error in field_errors:
                    messages.error(request, error)
        return redirect('infra-dashboard')


class TiNetworkNodeCreateView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        if not can_manage_sector(request.user, InfraSector.TI):
            messages.error(request, 'Apenas a TI ou coordenacao da infra pode gerenciar o mapa de rede.')
            return redirect('infra-dashboard')

        form = TiNetworkNodeForm(request.POST)
        if form.is_valid():
            node = form.save(commit=False)
            node.created_by = request.user
            node.save()
            messages.success(request, 'Ponto do mapeamento de rede cadastrado.')
        else:
            for field_errors in form.errors.values():
                for error in field_errors:
                    messages.error(request, error)
        return redirect('infra-dashboard')
