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
    visits.addNewVisit(request)
    resp = render(request, 'uskovapp/error.html', {'error': error})
    return resp

def views_image_view(request):
    visitshandler = visits.VisitsHandler()
    image = visitshandler.getImage()
    return HttpResponse(content=image, content_type='image/png')