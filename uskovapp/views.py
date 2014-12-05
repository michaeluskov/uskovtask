from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from datetime import datetime
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
    return render(request, 'uskovapp/comments.html')
    