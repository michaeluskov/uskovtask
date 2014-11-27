from django.shortcuts import render, render_to_response
from django.http import HttpResponse
import visits

# Create your views here.


def main(request):
    return render(request, 'uskovapp/main.html')

def photo(request):
    return render(request, 'uskovapp/photo.html')

def contacts(request):
    return render(request, 'uskovapp/contacts.html')  

def error_view(request, error=200):
    resp = render(request, 'uskovapp/error.html', {'error': error})
    return resp

def views_image_view(request):
    visitshandler = visits.VisitsHandler()
    image = visitshandler.getImage()
    return HttpResponse(content=image, content_type='image/png')