from models import Visits
from visits import getSessionsQuerySet, getAllIPsCount, getAllHitsCount


def addstats(request):
    allvisits = getAllHitsCount()
    ips = getAllIPsCount()
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