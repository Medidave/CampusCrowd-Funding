from pathlib import Path
import os 

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-)$s%c-*zz!gob-nk0qen^$vc7i5bk&g4_x2op@1f+60r7b7y3x'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'campuscrowd-8230c40f13a3.herokuapp.com',]


# Application definition

INSTALLED_APPS = [
    "daphne",
    'jazzmin',

    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google', 
    
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'CampusCrowd.apps.CampuscrowdConfig',
    'users.apps.UsersConfig',
    'CHAT_ROOM.apps.ChatRoomConfig',

]

SITE_ID = 2

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        },
    }
}

CSRF_TRUSTED_ORIGINS = ["https://campuscrowd-8230c40f13a3.herokuapp.com"]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]


ROOT_URLCONF = 'CampusCrowdFunding.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
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

WSGI_APPLICATION = 'CampusCrowdFunding.wsgi.application'
ASGI_APPLICATION = "CampusCrowdFunding.asgi.application"

# Channels layer settings
# CHANNEL_LAYERS = {
#     "default": {
#         "BACKEND": "channels_redis.core.RedisChannelLayer",
#         "CONFIG": {
#             "hosts": [os.environ.get('REDIS_URL', "redis://localhost:6379")],
#         },
#     },
# }

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [('127.0.0.1', 6379)],
        },
    },
}


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases   621754

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/images/'


STATICFILES_DIRS = [
    BASE_DIR /'static'
]

MEDIA_ROOT = os.path.join(BASE_DIR, 'static/images')
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# THE BELOW CODES REFER TO THE SETTING OF THE DJANGO STORAGES WHEN WE WANTED TO STORE OUR STATIC FILES LIKE IMAGES INTO S3 BUCKET
# DEFAULT_FILE_STORAGE = "storages.backends.s3.S3Storage"
# AWS_ACCESS_KEY_ID = 'Replace with aws secrete key id'
# AWS_SECRET_ACCESS_KEY = 'Replace with aws access key id' 
# AWS_STORAGE_BUCKET_NAME = 'Replace with aws bucket name'  #For security reasons i can't keep my bucket credentials and other credentials in the code
# AWS_QUERYSTRING_AUTH = False 
# AWS_S3_FILE_OVERWRITE = False 


# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT =  465
EMAIL_USE_TLS = False 
EMAIL_USE_SSL = True
EMAIL_HOST_USER = 'Replace with the mail address to send email to users'  # herh it finally worked la awwww
EMAIL_HOST_PASSWORD = 'Replace with the goggle app password that will allow email to be sent using the code'


# if os.getcwd() == '/app':
#     DEBUG = False

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'updates'
SOCIALACCOUNT_LOGIN_ON_GET = True
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'


# ACCOUNT_TEMPLATES = {
#     'account/signup': 'signup.html',
#     'account/login': 'login.html',
# }

ACCOUNT_FORMS = {
    'signup': 'users.forms.CustomSignupForm',
}

PAYSTACK_PUBLIC_KEY = 'Replace with your Paystack public key to get it working' 
PAYSTACK_SECRET_KEY = 'Replace with your Paystack secrete key to get it working'



