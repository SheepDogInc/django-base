from django.conf.urls import patterns, include, url
from django.contrib import admin

import visual_style.urls

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^visual-styles/', include(visual_style.urls)),
)
