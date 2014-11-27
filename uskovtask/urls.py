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

handler404 = lambda r: uskovviews.error_view(r, 404)
handler403 = lambda r: uskovviews.error_view(r, 403)
handler500 = lambda r: uskovviews.error_view(r, 500)
handler400 = lambda r: uskovviews.error_view(r, 400)
