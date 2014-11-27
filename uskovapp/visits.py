from models import Visits
from datetime import datetime, timedelta, date


def addNewVisit(request):
    visit = Visits()
    visit.ip = request.META['REMOTE_ADDR']
    visit.url = request.path
    visit.datetime = datetime.now()
    visit.save()    
    
    
def getSessionsQuerySet(customFilterForIP={}, customFilterForDates={}):
    sessions = []
    if len(customFilterForIP) > 0:
        query = Visits.objects.filter(**customFilter).values('ip').order_by().distinct()
    else:
        query = Visits.objects.values('ip').order_by().distinct()
    for ip in query:
        ip = ip['ip']
        if len(customFilterForDates) > 0:
            datetimeQuery = Visits.objects.filter(ip__exact=ip, **customFilterForDates).values('datetime')
        else:
            datetimeQuery = Visits.objects.filter(ip__exact=ip).values('datetime')
        allvisits = list(datetimeQuery)
        sessions.append({'ip': ip, 'datetime': allvisits[0]})
        allvisits = [i['datetime'] for i in allvisits]
        for second in xrange(1, len(allvisits)):
            first = second-1
            if (allvisits[second] - allvisits[first] >= timedelta(minutes=5)):
                sessions.append({'ip': ip, 'datetime': allvisits[second]})
    return sessions


def getAllIPsCount():
    return Visits.objects.values('ip').order_by().distinct().count()


def getAllHitsCount():
    return Visits.objects.count()


def getTodaySessions():
    return getSessionsQuerySet(customFilterForDates={'datetime__gte': date.today()})
    