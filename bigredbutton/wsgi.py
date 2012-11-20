"""
WSGI config for bigredbutton project.

This module contains the WSGI application used by Django's development server
and any production WSGI deployments. It should expose a module-level variable
named ``application``. Django's ``runserver`` and ``runfcgi`` commands discover
this application via the ``WSGI_APPLICATION`` setting.

Usually you will have the standard Django WSGI application here, but it also
might make sense to replace the whole Django WSGI application with a custom one
that later delegates to the Django one. For example, you could introduce WSGI
middleware here, or combine a Django application with an application of another
framework.

"""
import os, os.path
import sys
import site

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bigredbutton.settings")

project_path = os.path.realpath ( os.path.dirname(__file__) + "/../" )
vepath = os.path.realpath ( os.path.dirname(__file__) + "/../../../" )
vesite = os.path.realpath ( vepath + "/lib/python2.7/site-packages/" )

prev_sys_path = list(sys.path)

site.addsitedir(vesite)
sys.path.append ( project_path )

print sys.path

new_sys_path = [p for p in sys.path if p not in prev_sys_path]
for item in new_sys_path:
    sys.path.remove(item)
sys.path[:0] = new_sys_path

# This application object is used by any WSGI server configured to use this
# file. This includes Django's development server, if the WSGI_APPLICATION
# setting points here.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

import wsgi_monitor
wsgi_monitor.start(interval=5.0)

# Apply WSGI middleware here.
# from helloworld.wsgi import HelloWorldApplication
# application = HelloWorldApplication(application)
