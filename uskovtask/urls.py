from django.conf.urls import patterns, include, url

import uskovapp.views as uskovviews
from django.contrib.auth import views as authviews


from django.contrib import admin
from django.conf import settings
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^/?$', uskovviews.main, name='main'),
    url(r'^photo/', uskovviews.photo, name='photo'),
    url(r'^contacts/', uskovviews.contacts, name='contacts'),
    url(r'^views/image.png', uskovviews.views_image_view, name='views_image'),
    url(r'^views/addresolution', uskovviews.views_addresolution_view, name='views_addresolution'),
    url(r'^views/stats', uskovviews.views_view, name='views_view'),
    url(r'^views/ajax_visits', uskovviews.ajax_visits_view, name='views_ajax_visits'),
    url(r'^comments/history', uskovviews.comment_history_view, name='comment_history'),
    url(r'^comments/edit', uskovviews.edit_comment_view, name='edit_comment'),
    url(r'^comments/post', uskovviews.add_comment_view, name='add_comment'),
    url(r'^comments/', uskovviews.comments_view, name='comments'),
    url(r'^accounts/login', authviews.login, {'template_name': 'uskovapp/login.html'}, name='login'),
    url(r'^accounts/register', uskovviews.register_view, name='register'),
    url(r'^accounts/logout', authviews.logout, {'next_page': settings.LOGIN_URL}, name='logout'),
    url(r'^polls/vote', uskovviews.polls_vote_view, name='polls_vote'),
    url(r'^polls/unvote', uskovviews.polls_unvote_view, name='polls_unvote'),
    url(r'^polls/pic/(\d+).png', uskovviews.polls_pic_view, name='polls_pic'),
    url(r'^polls/', uskovviews.polls_view, name='polls'),
    url(r'^admin/', include(admin.site.urls)),
)

handler404 = lambda r: uskovviews.error_view(r, 404)
handler403 = lambda r: uskovviews.error_view(r, 403)
handler500 = lambda r: uskovviews.error_view(r, 500)
handler400 = lambda r: uskovviews.error_view(r, 400)
