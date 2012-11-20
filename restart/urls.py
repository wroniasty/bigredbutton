__author__ = 'kuba'

from django.conf.urls import patterns, include, url

urlpatterns = patterns('restart.views',
    url(r'^$', 'big_red_restart_button', name='index'),
    url(r'^do_it/(?P<vm_id>\d+)', 'do_restart', name='do_restart'),
)