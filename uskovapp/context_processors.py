from models import Visits
import visits


def addstats(request):
    allvisits = visits.getAllHitsCount()
    ips = visits.getAllIPsCount()
    sessionsQuerySet = visits.getSessionsQuerySet()
    allSessions = len(sessionsQuerySet)
    todaySessions = len(visits.getTodaySessions())
    lastSession = visits.getLastSession(request)
      
    return {
        'visits': {
            'all': allvisits,
            'ips': ips,
            'sessions': {
                'all': allSessions,
                'today': todaySessions,
                'last': lastSession
            }
        }
    }