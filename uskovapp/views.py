from django.shortcuts import render, render_to_response
from django.http import HttpResponse
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
    visitsHandler = visits.VisitsHandler()
    sessions_list = visitsHandler.getAllSessions()
    return render(request, 'uskovapp/views.html', {'sessions_list': sessions_list})


def views_image_view(request):
    visitshandler = visits.VisitsHandler()
    image = visitshandler.getImage()
    return HttpResponse(content=image, content_type='image/png')


def views_addresolution_view(request):
    if 'width' in request.GET and 'height' in request.GET:
        try:
            visits.addExtraInfoToVisit(request, int(request.GET['width']), int(request.GET['height']))
        except:
            pass
    return HttpResponse(content="{'status': 'OK'}", content_type='application/json')