from models import Visits
import datetime


def addNewVisit(request):
    visit = Visits()
    visit.ip = request.META['REMOTE_ADDR']
    visit.url = request.path
    visit.datetime = datetime.datetime.now()
    visit.save()    