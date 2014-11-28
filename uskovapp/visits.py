# -*- coding: utf-8 -*-

from models import Visits
from datetime import datetime, timedelta, date
from django.db.models import F
import user_agents
import PIL.Image
import PIL.ImageDraw
import PIL.ImageFont
import StringIO


def addNewVisit(request):
        visit = Visits()
        visit.ip = request.META['REMOTE_ADDR']
        visit.url = request.path
        visit.datetime = datetime.now()
        ua = user_agents.parse(request.META['HTTP_USER_AGENT'])
        visit.browser_name = ua.browser.family
        visit.browser_version = ua.browser.version_string
        visit.save()

def addExtraInfoToVisit(request, width, height):
        res_string = '%sx%s' % (width, height)
        lastReq = Visits.objects.filter(ip__exact='127.0.0.1').order_by('-datetime').all()[:1][0]
        lastReq.resolution = res_string
        lastReq.save()
        

class VisitsHandler:
    
    def __init__(self):
        self.query = self.getSessionsQuerySet()

    def getSessionsQuerySet(self, customFilterForIP={}, customFilterForDates={}):
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

    def getAllSessions(self):
        return self.query
      
    def getAllIPsCount(self):
        ips = {}
        for x in self.query:
                ips[x['ip']] = 1
        return len(ips)
      
    def getAllHitsCount(self):
        return Visits.objects.count()

    def getTodaySessions(self):
        sessions = []
        for x in self.query:
            if x['datetime'].date() == date.today():
                sessions.append(x)
        return sessions
       
    def getLastSession(self):
        maxdatetime = datetime(1970, 1, 1)
        for x in self.query:
            if x['datetime'] > maxdatetime:
                maxdatetime = x['datetime']
        return maxdatetime.strftime('%d.%m.%y %H:%M:%S')

    def getImage(self):
        image = PIL.Image.new('RGB', (155, 45), '#ffffff')
        font = PIL.ImageFont.truetype('uskovapp/Helvetica_Light-Normal.ttf', size=12, encoding='utf-8')
        draw = PIL.ImageDraw.Draw(image)
        draw.text((3,3), u'Всего: ' + unicode(len(self.getAllSessions())), fill='#000000', font=font)
        draw.text((3,18), u'Сегодня: ' + unicode(len(self.getTodaySessions())), fill='#000000', font=font)
        draw.text((3,33), u'Последний: ' + unicode(self.getLastSession()), fill='#000000', font=font)
        string = StringIO.StringIO()
        image.save(string, 'PNG')
        return string.getvalue()


    