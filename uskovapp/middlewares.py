from models import Visits
import datetime 


class VisitsMiddleware:
    
    def process_request(self, request):
        visit = Visits()
        visit.ip = request.META['REMOTE_ADDR']
        visit.url = request.path
        visit.datetime = datetime.datetime.now()
        visit.save()
        return None
