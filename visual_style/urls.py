from django.conf.urls import patterns, include, url

from . import views


urlpatterns = patterns('',
    url(r'^$', views.VisualStyleView.as_view(), name="visual-style"),
)
