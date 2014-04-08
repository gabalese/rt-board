from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^ping/$', 'haas.views.ping'),
                       url(r'^messages/$', 'haas.views.submit_message'),
                       url(r'^messages/(.+)$', 'haas.views.show_single_message'),
                       url(r'^updates/(\d+)$', 'haas.views.updates_show'),
                       url(r'^$', 'haas.views.main_view'))