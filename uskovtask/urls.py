from django.conf.urls import patterns, include, url

import uskovapp.views as uskovviews

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^/?$', uskovviews.main, name='main'),
    url(r'^photo/', uskovviews.photo, name='photo'),
    url(r'^contacts/', uskovviews.contacts, name='contacts'),
    #url(r'^admin/', include(admin.site.urls)),
)

handler404 = uskovviews.error_view
handler403 = uskovviews.error_view
handler500 = uskovviews.error_view
handler400 = uskovviews.error_view
