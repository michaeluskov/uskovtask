from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.db.models import Max, Count
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.views.decorators.cache import cache_control
import random

from uskovapp.models import Comments, CommentVersions, Polls, PollVariants, Votes
from uskovapp.poll_picture import createPollPic
import visits

# Create your views here.


def main(request):
    visits.addNewVisit(request)
    return render(request, 'uskovapp/main.html')


def photo(request):
    visits.addNewVisit(request)
    return render(request, 'uskovapp/photo.html')


def contacts(request):
    visits.addNewVisit(request)
    return render(request, 'uskovapp/contacts.html')


def error_view(request, error=200):
    resp = render(request, 'uskovapp/error.html', {'error': error})
    resp.status_code = error
    return resp


def views_view(request):
    visits.addNewVisit(request)
    sessions_list = reversed(list(visits.getAllSessions()))
    return render(request, 'uskovapp/views.html', {'sessions_list': sessions_list})


def ajax_visits_view(request):
    try:
        sessionVisits = visits.getAllVisitsFromSession(request.GET['id'])
    except Exception as e:
        sessionVisits = []
    finally:
        return render(request, 'uskovapp/views_session.html', {'visits': sessionVisits})


@cache_control(max_age=0, no_cache=True, no_store=True, must_revalidate=True)
def views_image_view(request):
    image = visits.getImage()
    return HttpResponse(content=image, content_type='image/png')


def views_addresolution_view(request):
    if 'width' in request.GET and 'height' in request.GET:
        try:
            visits.addExtraInfoToVisit(request, int(request.GET['width']), int(request.GET['height']))
        except:
            pass
    return HttpResponse(content="{'status': 'OK'}", content_type='application/json')


def comments_view(request):
    visits.addNewVisit(request)
    actualPKs = CommentVersions.objects.values('comment__id').annotate(actual=Max('id')).values('actual')
    commentQuery = CommentVersions.objects.filter(pk__in=actualPKs).order_by('-comment__datetime')
    return render(request, 'uskovapp/comments.html', {'comments': commentQuery})


def register_view(request):
    redirect_url = request.GET.get('next', None) or request.POST.get('next', None) or settings.LOGIN_URL
    if request.method != 'POST':
        return HttpResponseRedirect(redirect_url)
    try:
        if not User.objects.filter(username=request.POST['username']).exists():
            User.objects.create_user(request.POST['username'], 
                                     password=request.POST['password'])
            user = authenticate(username=request.POST['username'], 
                                password=request.POST['password'])
            login(request, user)
            return HttpResponseRedirect(redirect_url)
        else:
            return HttpResponseRedirect(redirect_url)
    except Exception as e:
        return HttpResponseRedirect(redirect_url)
    
    
def add_comment_view(request):
    if request.method != 'POST' or not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('comments'))
    try:
        if request.POST.get('text', '') == '':
            return HttpResponseRedirect(reverse('comments'))
        if Comments.objects.filter(user=request.user,
                                   datetime__gte=timezone.datetime.now() \
                                   -timezone.timedelta(minutes=1)).exists():
            return HttpResponseRedirect(reverse('comments'))
        comment = Comments(user=request.user, datetime=timezone.datetime.now())
        comment.save()
        version = CommentVersions(comment=comment, text=request.POST['text'], datetime=timezone.datetime.now())
        version.save()
        return HttpResponseRedirect(reverse('comments'))
    except Exception as e:
        return HttpResponseRedirect(reverse('comments'))
    
def comment_history_view(request):
    try:
        visits.addNewVisit(request)
        versions = CommentVersions.objects.filter(comment__user=request.user, 
                                                  comment__pk=request.GET['id']).order_by('-datetime')
        return render(request, 'uskovapp/comment_history.html', {'comments': versions})
    except Exception as e:
        return HttpResponseRedirect(reverse('comments'))
    

def edit_comment_view(request):
    if request.method != 'POST' or not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('comments'))
    try:
        if request.POST.get('text', '') == '':
            return HttpResponseRedirect(reverse('comments'))        
        comment = Comments.objects.filter(user=request.user,
                                          pk=request.POST['id'])[0]
        comment.commentversions_set.create(datetime=timezone.datetime.now(),
                                           text=request.POST['text'])
        return HttpResponseRedirect(reverse('comments'))
    except Exception as e:
        return HttpResponseRedirect(reverse('comments'))
    
    
def polls_view(request):
    visits.addNewVisit(request);
    polls = Polls.objects.all().annotate(votes_count=Count('pollvariants__votes'))
    polls_user_voted = Votes.objects.filter(user__username=request.user.username).values('variant__poll__pk')
    polls_user_voted = [i['variant__poll__pk'] for i in polls_user_voted]
    return render(request, 'uskovapp/polls.html', {'polls': polls,
                                                   'polls_user_voted': polls_user_voted
                                                   })

def polls_vote_view(request):
    if ('poll' not in request.GET or 'variant' not in request.GET):
        return HttpResponse(content='')
    poll_pk = request.GET.get('poll',-1)
    variant_pk = request.GET.get('variant',-1)
    if Votes.objects.filter(user__username = request.user.username, variant__poll__pk = poll_pk).exists():
        poll = Polls.objects.get(pk=poll_pk)
        return render(request, 'uskovapp/onepoll.html', {'poll': poll, 
                                                         'user_voted': 1})
    if not PollVariants.objects.filter(pk=variant_pk, poll_id=poll_pk).exists():
        return HttpResponse(content='')
    p = Votes(user = request.user, variant_id = variant_pk, datetime = timezone.now())
    p.save()
    poll = Polls.objects.get(pk=poll_pk)
    return render(request, 'uskovapp/onepoll.html', {'poll': poll, 
                                                     'user_voted': 1})

def polls_unvote_view(request):
    if ('poll' not in request.GET):
            return HttpResponse(content='')
    poll_pk = request.GET['poll']
    Votes.objects.filter(user__username = request.user.username, 
                         variant__poll__pk = poll_pk).delete()
    if not Polls.objects.filter(pk=poll_pk).exists():
        return HttpResponse(content='')
    poll = Polls.objects.get(pk=poll_pk)
    return render(request, 'uskovapp/onepoll.html', {'poll': poll, 
                                                     'user_voted': 0})

@cache_control(max_age=0, no_cache=True, no_store=True, must_revalidate=True)
def polls_pic_view(request, poll_pk):
    if not Polls.objects.filter(pk=poll_pk).exists():
        raise Http404
    pic = createPollPic(poll_pk)
    return HttpResponse(content=pic, content_type='image/png')