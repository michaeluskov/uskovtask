from django.shortcuts import render, render_to_response

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