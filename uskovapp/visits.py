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
        allvisits = [i['datetime'] for i in allvisits]
        sessions.append({'ip': ip, 'datetime': allvisits[0]})
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


def getLastSession(request):
    query = getSessionsQuerySet()
    maxdatetime = datetime(1970, 1, 1)
    
    for x in query:
        if x['datetime'] > maxdatetime:
            maxdatetime = x['datetime']
    return maxdatetime.strftime('%d.%m.%y %H:%M:%S')


    