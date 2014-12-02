from models import Visits
from visits import addNewVisit
import datetime 
import traceback
import sys


class VisitsMiddleware:
    
    def process_request(self, request):
        addNewVisit(request)
        return None
    
    
class ErrorMiddleware:
    
    def process_exception(self, request, exception):
        sys.stderr.write(traceback.format_exc())
        sys.stderr.flush()
        