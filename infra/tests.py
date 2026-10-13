from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from accounts.models import User

from .models import InfraCalendarEvent, InfraRequest, InfraRequestUpdate, InfraSector, TiInventoryItem, TiNetworkNode


class InfraFlowTests(TestCase):
    password = 'SenhaSegura!2026'

    def setUp(self):
        self.member = User.objects.create_user(
            username='usuario.infra',
            display_name='Usuario Infra',
            handle='usuario_infra',
            email='usuario.infra@example.com',
            password=self.password,
        )
        self.ti_operator = User.objects.create_user(
            username='ti.infra',
            display_name='Operador de TI',
            handle='ti_infra',
            email='ti.infra@example.com',
            is_infra_ti_operator=True,
            password=self.password,
        )
        self.coordinator = User.objects.create_user(
            username='coord.infra',
            display_name='Coordenacao da Infra',
            handle='coord_infra',
            email='coord.infra@example.com',
            is_infra_coordinator=True,
            password=self.password,
        )

    def test_user_creates_ti_request_and_operator_schedules_it(self):
        self.client.force_login(self.member)
        response = self.client.post(
            reverse('infra-request-create'),
            {
                'sector': InfraSector.TI,
                'category': InfraRequest.Category.COMPUTER,
                'title': 'Computador da biblioteca nao liga',
                'location': 'Biblioteca',
                'asset_identifier': 'PC-BIB-01',
                'priority': InfraRequest.Priority.HIGH,
                'description': 'A maquina usada pelos operadores nao liga desde ontem.',
            },
        )
        self.assertRedirects(response, reverse('infra-dashboard'))
        infra_request = InfraRequest.objects.get(title='Computador da biblioteca nao liga')
        self.assertEqual(infra_request.requester, self.member)
        self.assertTrue(InfraRequestUpdate.objects.filter(request=infra_request).exists())

        self.client.force_login(self.ti_operator)
        scheduled_for = timezone.now().replace(microsecond=0) + timezone.timedelta(days=1)
        response = self.client.post(
            reverse('infra-request-manage', args=[infra_request.pk]),
            {
                'status': InfraRequest.Status.SCHEDULED,
                'priority': InfraRequest.Priority.HIGH,
                'assigned_to': self.ti_operator.pk,
                'scheduled_for': scheduled_for.strftime('%Y-%m-%dT%H:%M'),
            },
        )
        self.assertRedirects(response, reverse('infra-dashboard'))
        infra_request.refresh_from_db()
        self.assertEqual(infra_request.status, InfraRequest.Status.SCHEDULED)
        self.assertEqual(infra_request.assigned_to, self.ti_operator)

        self.client.force_login(self.member)
        response = self.client.get(reverse('infra-dashboard'))
        self.assertContains(response, 'Computador da biblioteca nao liga')
        self.assertContains(response, 'Solicitacao atualizada pela infra.')

    def test_non_operator_cannot_manage_sector_request(self):
        infra_request = InfraRequest.objects.create(
            requester=self.member,
            sector=InfraSector.TI,
            category=InfraRequest.Category.WIFI,
            title='Wi-Fi da secretaria caiu',
            location='Secretaria',
            description='Rede da secretaria sem acesso.',
        )
        self.client.force_login(self.member)
        response = self.client.post(
            reverse('infra-request-manage', args=[infra_request.pk]),
            {
                'status': InfraRequest.Status.DONE,
                'priority': InfraRequest.Priority.NORMAL,
                'assigned_to': '',
                'scheduled_for': '',
            },
        )
        self.assertRedirects(response, reverse('infra-dashboard'))
        infra_request.refresh_from_db()
        self.assertEqual(infra_request.status, InfraRequest.Status.NEW)

    def test_coordinator_creates_shared_calendar_event(self):
        self.client.force_login(self.coordinator)
        start_at = timezone.now().replace(microsecond=0) + timezone.timedelta(days=2)
        response = self.client.post(
            reverse('infra-calendar-create'),
            {
                'sector': InfraSector.MAINTENANCE,
                'title': 'Revisao hidraulica do bloco central',
                'start_at': start_at.strftime('%Y-%m-%dT%H:%M'),
                'end_at': '',
                'location': 'Bloco central',
                'responsible': self.coordinator.pk,
                'status': InfraCalendarEvent.Status.CONFIRMED,
                'notes': 'Checar vazamentos e registros.',
            },
        )
        self.assertRedirects(response, reverse('infra-dashboard'))
        self.assertTrue(InfraCalendarEvent.objects.filter(title='Revisao hidraulica do bloco central').exists())

    def test_sector_tab_uses_card_model_for_every_sector(self):
        self.client.force_login(self.coordinator)

        response = self.client.get(reverse('infra-dashboard'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Rede Wi-Fi e internet')
        self.assertContains(response, 'Ciclo agricola')
        self.assertContains(response, 'Jardins e areas verdes')
        self.assertContains(response, 'Hidraulica e eletrica')
        self.assertContains(response, 'infra-sector-producao')
        self.assertContains(response, 'infra-sector-jardinagem')
        self.assertContains(response, 'infra-sector-manutencao')

    def test_user_creates_direct_ti_ticket(self):
        self.client.force_login(self.member)

        response = self.client.post(
            reverse('infra-ti-ticket-create'),
            {
                'category': InfraRequest.Category.WIFI,
                'title': 'Wi-Fi do laboratorio caiu',
                'location': 'Laboratorio',
                'asset_identifier': 'Rede Escola',
                'priority': InfraRequest.Priority.URGENT,
                'description': 'A rede esta sem conexao durante a oficina.',
            },
        )

        self.assertRedirects(response, reverse('infra-dashboard'))
        ticket = InfraRequest.objects.get(title='Wi-Fi do laboratorio caiu')
        self.assertEqual(ticket.sector, InfraSector.TI)
        self.assertEqual(ticket.requester, self.member)
        self.assertTrue(
            InfraRequestUpdate.objects.filter(
                request=ticket,
                body='Chamado direto de TI aberto pelo usuario.',
            ).exists()
        )

    def test_ti_operator_creates_inventory_and_network_nodes(self):
        self.client.force_login(self.ti_operator)

        response = self.client.post(
            reverse('infra-ti-inventory-create'),
            {
                'name': 'PC-BIB-02',
                'kind': TiInventoryItem.Kind.DESKTOP,
                'asset_code': 'PAT-002',
                'location': 'Biblioteca',
                'assigned_to': self.member.pk,
                'ip_address': '10.0.0.22',
                'mac_address': 'AA:BB:CC:DD:EE:02',
                'operating_system': 'Linux Mint',
                'status': TiInventoryItem.Status.ACTIVE,
                'notes': 'Computador usado no atendimento da biblioteca.',
            },
        )
        self.assertRedirects(response, reverse('infra-dashboard'))
        inventory_item = TiInventoryItem.objects.get(name='PC-BIB-02')
        self.assertEqual(inventory_item.created_by, self.ti_operator)
        self.assertEqual(inventory_item.assigned_to, self.member)

        response = self.client.post(
            reverse('infra-ti-network-create'),
            {
                'name': 'AP Biblioteca',
                'kind': TiNetworkNode.Kind.ACCESS_POINT,
                'location': 'Biblioteca',
                'ip_address': '10.0.0.2',
                'ssid': 'Escola-Biblioteca',
                'vlan': 'VLAN 20',
                'upstream': 'Switch central',
                'status': TiNetworkNode.Status.ACTIVE,
                'notes': 'Cobertura da biblioteca e sala de leitura.',
            },
        )
        self.assertRedirects(response, reverse('infra-dashboard'))
        network_node = TiNetworkNode.objects.get(name='AP Biblioteca')
        self.assertEqual(network_node.created_by, self.ti_operator)

    def test_member_cannot_manage_ti_inventory(self):
        self.client.force_login(self.member)

        response = self.client.post(
            reverse('infra-ti-inventory-create'),
            {
                'name': 'PC-SEM-PERMISSAO',
                'kind': TiInventoryItem.Kind.DESKTOP,
                'asset_code': '',
                'location': 'Secretaria',
                'assigned_to': '',
                'ip_address': '',
                'mac_address': '',
                'operating_system': '',
                'status': TiInventoryItem.Status.ACTIVE,
                'notes': '',
            },
        )

        self.assertRedirects(response, reverse('infra-dashboard'))
        self.assertFalse(TiInventoryItem.objects.filter(name='PC-SEM-PERMISSAO').exists())

    def test_dashboard_renders_ti_operations_tabs_for_operator(self):
        TiInventoryItem.objects.create(
            name='PC-BIB-03',
            kind=TiInventoryItem.Kind.DESKTOP,
            asset_code='PAT-003',
            location='Biblioteca',
            status=TiInventoryItem.Status.ACTIVE,
            created_by=self.ti_operator,
        )
        TiNetworkNode.objects.create(
            name='Roteador central',
            kind=TiNetworkNode.Kind.ROUTER,
            location='Bloco central',
            ip_address='10.0.0.1',
            status=TiNetworkNode.Status.ACTIVE,
            created_by=self.ti_operator,
        )
        self.client.force_login(self.ti_operator)

        response = self.client.get(reverse('infra-dashboard'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Computadores e servidores')
        self.assertContains(response, 'Mapa de rede')
        self.assertContains(response, 'Abrir chamado para a TI')
        self.assertContains(response, 'PC-BIB-03')
        self.assertContains(response, 'Roteador central')
