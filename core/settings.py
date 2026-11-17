import os, dj_database_url, cloudinary
from pathlib import Path


# ==========================================================
# CAMINHOS DO PROJETO
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

from dotenv import load_dotenv

load_dotenv(BASE_DIR / '.env')


# ==========================================================
# SEGURANÇA
# ==========================================================

# No computador, utiliza a chave local.
# Na Vercel, utiliza a variável de ambiente SECRET_KEY.
SECRET_KEY = os.environ.get(
    'SECRET_KEY',
    'django-insecure-chave-apenas-para-desenvolvimento'
)

# DEBUG fica ativado localmente e desativado na Vercel.
DEBUG = os.environ.get('VERCEL') != '1'

# Domínios autorizados a acessar o projeto.
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '.vercel.app']

# Endereços autorizados a enviar formulários para o Django.
CSRF_TRUSTED_ORIGINS = [
    'https://*.vercel.app',
]


# ==========================================================
# APLICATIVOS
# ==========================================================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Cloudinary
    'cloudinary_storage',
    'cloudinary',

    # Aplicativos do projeto
    'categorias',
    'receitas',
    'ingredientes',
    'frontend',
    'painel',
]


# ==========================================================
# MIDDLEWARE
# ==========================================================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',

    # Serve arquivos CSS, JavaScript e outros arquivos estáticos.
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# ==========================================================
# URLS E TEMPLATES
# ==========================================================

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'





# BANCO DE DADOS

DATABASE_URL = os.environ.get('DATABASE_URL')

if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=0,
            ssl_require=True,
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }



# ==========================================================
# SENHAS
# ==========================================================

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# ==========================================================
# IDIOMA E HORÁRIO
# ==========================================================

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_TZ = True


# ==========================================================
# ARQUIVOS ESTÁTICOS E MÍDIA
# ==========================================================

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# ==========================================================
# CLOUDINARY
# ==========================================================

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.getenv('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': os.getenv('CLOUDINARY_API_KEY'),
    'API_SECRET': os.getenv('CLOUDINARY_API_SECRET'),
    'SECURE': True,
}

# Configuração do SDK do Cloudinary.
cloudinary.config(
    cloud_name=CLOUDINARY_STORAGE['CLOUD_NAME'],
    api_key=CLOUDINARY_STORAGE['API_KEY'],
    api_secret=CLOUDINARY_STORAGE['API_SECRET'],
    secure=True,
)

STORAGES = {
    'default': {
        'BACKEND': 'cloudinary_storage.storage.MediaCloudinaryStorage',
    },
    'staticfiles': {
        'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage',
    },
}


# ==========================================================
# ARQUIVOS DE MÍDIA (IMAGENS ENVIADAS PELO ADMIN)
# ==========================================================

MEDIA_URL = '/media/'

MEDIA_ROOT = BASE_DIR / 'media'


# ==========================================================
# E-MAIL
# ==========================================================

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# ==========================================================
# PERSONALIZAÇÃO DO ADMIN
# ==========================================================

ADMIN_SITE_HEADER = 'Administração de Receitas'
ADMIN_SITE_TITLE = 'Painel de Receitas'
ADMIN_INDEX_TITLE = 'Gerenciamento do site'


# ==========================================================
# AUTENTICAÇÃO
# ==========================================================

LOGIN_URL = 'painel:login'

LOGIN_REDIRECT_URL = 'painel:dashboard'

LOGOUT_REDIRECT_URL = 'painel:login'


# ==========================================================
# CONFIGURAÇÕES GERAIS
# ==========================================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

