from .base import *

DEBUG = True

ALLOWED_HOSTS = []

SECRET_KEY = 'l@%PKs7u`.zZ,v4)Hw&A-gCR]Zt.2"3dQ1#0lZ>fZSK*r8]?C'

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'dev_db.sqlite3',
    }
}
