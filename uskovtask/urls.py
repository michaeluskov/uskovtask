from django.conf.urls import patterns, include, url

import uskovapp.views as uskovviews

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^/?$', uskovviews.main, name='main'),
    url(r'^photo/', uskovviews.photo, name='photo'),
    url(r'^contacts/', uskovviews.contacts, name='contacts'),
    url(r'^views/image.png', uskovviews.views_image_view, name='views_image'),
    url(r'^views/addresolution', uskovviews.views_addresolution_view, name='views_addresolution'),
    url(r'^views/stats', uskovviews.views_view, name='views_view'),
    url(r'^views/ajax_visits', uskovviews.ajax_visits_view, name='views_ajax_visits')
    #url(r'^admin/', include(admin.site.urls)),
)

handler404 = lambda r: uskovviews.error_view(r, 404)
handler403 = lambda r: uskovviews.error_view(r, 403)
handler500 = lambda r: uskovviews.error_view(r, 500)
handler400 = lambda r: uskovviews.error_view(r, 400)
