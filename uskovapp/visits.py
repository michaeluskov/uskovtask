from models import Visits
from datetime import datetime, timedelta


def addNewVisit(request):
    visit = Visits()
    visit.ip = request.META['REMOTE_ADDR']
    visit.url = request.path
    visit.datetime = datetime.now()
    visit.save()    
    
def getSessionsQuerySet():
    sessions = []
    for ip in Visits.objects.values('ip').order_by().distinct():
        ip = ip['ip']
        allvisits = list(Visits.objects.filter(ip__exact=ip).values('datetime'))
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