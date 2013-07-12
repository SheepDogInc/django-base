from ..base import *

import dj_database_url
DATABASES['default'] = dj_database_url.config()

COMPRESS_ENABLED = True
COMPRESS_OFFLINE = True

S3_BACKEND = 'storages.backends.s3boto.S3BotoStorage'
DEFAULT_FILE_STORAGE = S3_BACKEND
STATICFILES_STORAGE = S3_BACKEND
COMPRESS_STORAGE = S3_BACKEND

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_QUERYSTRING_AUTH = False
AWS_STORAGE_BUCKET_NAME = '%s-assets' % PROJECT_NAME