from config.settings.base import *

# Application definition
DEBUG = False
ALLOWED_HOSTS = get_secret('ALLOWED_HOSTS')

# Logging definition
LOGGING_DIR = os.path.join(BASE_DIR, 'tmp/logs')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'class': 'logging.FileHandler',
            'level': 'WARNING',
            'filename': os.path.join(LOGGING_DIR, 'django.log'),
        },
    },
    'loggers': {
        '': {
            'handlers': ['file'],
            'propagate': True,
            'level': 'INFO',
        },
    }
}
