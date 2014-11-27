from models import Visits
from visits import addNewVisit
import datetime 


class VisitsMiddleware:
    
    def process_request(self, request):
        addNewVisit(request)
        return None
