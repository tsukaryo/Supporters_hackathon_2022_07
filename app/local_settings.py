import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'django-insecure-@ch$t1lgwme$h&&r*w8mj*bt=gh4+z_ift_@db%_*s3@*o*$4y' #追加

 #settings.pyからそのままコピー
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'django-db',
        'USER': 'django',
        'PASSWORD': 'django',
        'HOST': 'db',
        'PORT': '3306'
    }
}

DEBUG = True