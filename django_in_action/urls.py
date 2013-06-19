from django.conf.urls import patterns, include, url
from django.contrib import admin
from views import login_view, logout_view

admin.autodiscover()

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'django_in_action.views.home', name='home'),
    # url(r'^django_in_action/', include('django_in_action.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^depotapp/', include('depotapp.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    (r'^accounts/login/$', login_view),
    (r'^accounts/logout/$', logout_view),
)

#5
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()
