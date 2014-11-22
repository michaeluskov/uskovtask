from django.core.handlers.wsgi import WSGIHandler
import django
import os

class WSGIEnvironment(WSGIHandler):

    def __call__(self, environ, start_response):

        if 'USKOVTASK_PROD' in environ:
            os.environ['USKOVTASK_PROD'] = environ['USKOVTASK_PROD']
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "uskovtask.settings")
        django.setup()
        return super(WSGIEnvironment, self).__call__(environ, start_response)

application = WSGIEnvironment()