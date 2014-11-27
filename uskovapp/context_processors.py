from models import Visits
import visits


def addstats(request):
    visitshandler = visits.VisitsHandler()
    allvisits = visitshandler.getAllHitsCount()
    ips = visitshandler.getAllIPsCount()
    sessionsQuerySet = visitshandler.getSessionsQuerySet()
    allSessions = len(sessionsQuerySet)
    todaySessions = len(visitshandler.getTodaySessions())
    lastSession = visitshandler.getLastSession(request)
      
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