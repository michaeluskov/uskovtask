from models import Visits


def addstats(request):
    allvisits = Visits.objects.count()
    ips = Visits.objects.values('ip').order_by().distinct().count()
      
    return {
        'visits': {
            'all': allvisits,
            'ips': ips,
        }
    }