from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^ping/$', 'messaging.views.ping'),
                       url(r'^messages/$', 'messaging.views.submit_message'),
                       url(r'^messages/(.+)$', 'messaging.views.show_single_message'),
                       url(r'^updates/(\d+)$', 'messaging.views.updates_show'),
                       url(r'^$', 'messaging.views.main_view'))