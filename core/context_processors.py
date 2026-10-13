from django.conf import settings


def site_identity(request):
    return {
        'SITE_NAME': getattr(settings, 'SITE_NAME', 'Rede Raizes Socialista'),
        'SITE_DESCRIPTION': getattr(settings, 'SITE_DESCRIPTION', ''),
        'SIGNUP_INVITE_ONLY': getattr(settings, 'SIGNUP_INVITE_ONLY', False),
    }
