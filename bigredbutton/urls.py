from django.conf.urls import patterns, include, url
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'bigredbutton.views.home', name='home'),
    # url(r'^bigredbutton/', include('bigredbutton.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^$', lambda x: HttpResponseRedirect(reverse('restart:index'))),
    url(r'^restart/', include('restart.urls', namespace='restart')),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout_then_login', name='logout'),
    url(r'^accounts/profile/$', lambda x: HttpResponseRedirect(reverse('restart:index'))),
)

