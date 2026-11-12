from django.contrib import admin
from django.urls import include, path

from core.views import (
    HomeView,
    ProtectedMediaView,
    SecurityCenterView,
    SecurityInviteCreateView,
    SecurityInviteRevokeView,
    SecurityPasswordRequestActionView,
    SecurityUserEditView,
    SecurityUserStatusToggleView,
)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('i18n/', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),
    path('conta/', include('accounts.urls')),
    path('feed/', include('social.urls')),
    path('mensagens/', include('messaging.urls')),
    path('saude/', include('health.urls')),
    path('almoxarifado/', include('warehouse.urls')),
    path('infra/', include('infra.urls')),
    path('financeiro/', include('finance.urls')),
    path(
        'arquivos/<slug:kind>/<int:object_id>/<slug:action>/<str:token>/',
        ProtectedMediaView.as_view(),
        name='protected-media',
    ),
    path('seguranca/', SecurityCenterView.as_view(), name='security-center'),
    path('seguranca/convites/', SecurityInviteCreateView.as_view(), name='security-invite-create'),
    path('seguranca/convites/<int:pk>/revogar/', SecurityInviteRevokeView.as_view(), name='security-invite-revoke'),
    path('seguranca/usuarios/<int:pk>/editar/', SecurityUserEditView.as_view(), name='security-user-edit'),
    path('seguranca/usuarios/<int:pk>/status/', SecurityUserStatusToggleView.as_view(), name='security-user-toggle'),
    path(
        'seguranca/solicitacoes-senha/<int:pk>/<slug:action>/',
        SecurityPasswordRequestActionView.as_view(),
        name='security-password-request-action',
    ),
]
