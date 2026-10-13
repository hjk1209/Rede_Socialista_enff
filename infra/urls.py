from django.urls import path

from .views import (
    InfraCalendarEventCreateView,
    InfraDashboardView,
    InfraRequestCreateView,
    InfraRequestManageView,
    InfraRequestUpdateCreateView,
    TiInventoryItemCreateView,
    TiNetworkNodeCreateView,
    TiSupportRequestCreateView,
)


urlpatterns = [
    path('', InfraDashboardView.as_view(), name='infra-dashboard'),
    path('solicitacoes/criar/', InfraRequestCreateView.as_view(), name='infra-request-create'),
    path('solicitacoes/<int:pk>/conversar/', InfraRequestUpdateCreateView.as_view(), name='infra-request-update'),
    path('solicitacoes/<int:pk>/gerenciar/', InfraRequestManageView.as_view(), name='infra-request-manage'),
    path('calendario/criar/', InfraCalendarEventCreateView.as_view(), name='infra-calendar-create'),
    path('ti/chamados/criar/', TiSupportRequestCreateView.as_view(), name='infra-ti-ticket-create'),
    path('ti/inventario/criar/', TiInventoryItemCreateView.as_view(), name='infra-ti-inventory-create'),
    path('ti/rede/criar/', TiNetworkNodeCreateView.as_view(), name='infra-ti-network-create'),
]
