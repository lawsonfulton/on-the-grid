from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^vendorlist/', include('vendorlist.urls')),
    #url(r'^admin/', include(admin.site.urls)),
)
