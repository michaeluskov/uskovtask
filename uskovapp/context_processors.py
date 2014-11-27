from models import Visits
from django.db.models import Q
from datetime import timedelta


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


def addstats(request):
    allvisits = Visits.objects.count()
    ips = Visits.objects.values('ip').order_by().distinct().count()
    sessionsQuerySet = getSessionsQuerySet()
    allSessions = len(sessionsQuerySet)
      
    return {
        'visits': {
            'all': allvisits,
            'ips': ips,
            'sessions': {
                'all': allSessions,
            }
        }
    }