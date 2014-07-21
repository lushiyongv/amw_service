import os,sys
activate_this = '/home/wwwroot/briapp/.venv/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))
reload(sys)

if not os.path.dirname(__file__) in sys.path[:1]:
    sys.path.insert(0, os.path.dirname(__file__))
os.environ['DJANGO_SETTINGS_MODULE'] = 'amway_service.settings'

from django.core.handlers.wsgi import WSGIHandler
application = WSGIHandler()