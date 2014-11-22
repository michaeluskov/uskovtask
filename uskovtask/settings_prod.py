DEBUG = False

TEMPLATE_DEBUG = False

ALLOWED_HOSTS = ['.uskovtask.mooo.com']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'uskovtask',
        'USER': 'uskovtask',
        'PASSWORD': '65e65e',
        'HOST': 'localhost',
    }
}

STATIC_ROOT = '/mnt/ebs/uskovtask/static'