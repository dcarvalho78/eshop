# ecommerce/settings.py

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third-party apps
    'parler',
    
    # Local apps (nur einmal registrieren!)
    'myapp.apps.MyappConfig',  # Deine Hauptapp
    'orders.apps.OrdersConfig',  # Orders App (nur diese Form verwenden)
    'cart.apps.CartConfig',
   # 'payments.apps.PaymentsConfig',

]

# Sicherstellen, dass alle Apps eindeutige Namen haben
for app in INSTALLED_APPS:
    assert INSTALLED_APPS.count(app) == 1, f"Doppelte App gefunden: {app}"

# Parler Einstellungen (für Übersetzungen)
PARLER_LANGUAGES = {
    None: (
        {'code': 'de'},
        {'code': 'en'},
    ),
    'default': {
        'fallback': 'de',
        'hide_untranslated': False,
    }
}

# Wichtig: Pfade müssen korrekt sein
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Media Files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Static Files
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# Am besten in settings.py:
DEBUG = os.environ.get('DJANGO_DEBUG', 'True') == 'True'

ALLOWED_HOSTS = ['*'] if DEBUG else [
    'deine-domain.de',
    'www.deine-domain.de',
    'localhost',
    '127.0.0.1'
]
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]