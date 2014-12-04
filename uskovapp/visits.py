# -*- coding: utf-8 -*-

from models import Visits, Sessions
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
    if Visits.objects.filter(ip__exact=request.META['REMOTE_ADDR']).exists():
        lastVisit = Visits.objects.filter(ip__exact=request.META['REMOTE_ADDR']).order_by('-datetime')[:1][0] 
        if datetime.now() - timedelta(minutes=5) > lastVisit.datetime:
            session = Sessions(ip=request.META['REMOTE_ADDR'], datetime=datetime.now())
            session.save()
        else:
            session = lastVisit.session
    else:
        session = Sessions(ip=request.META['REMOTE_ADDR'], datetime=datetime.now())
        session.save()
    visit.session = session
    visit.save()
    
    
def getAllSessions():
    return Sessions.objects.all()


def getTodaySessions():
    return Sessions.objects.filter(datetime__gte=date.today())

def getLastSessionDatetime():
    return Sessions.objects.order_by('-datetime').values('datetime')[:1][0]['datetime'].strftime('%d.%m.%Y %H:%M:%S')

def addExtraInfoToVisit(request, width, height):
    res_string = '%sx%s' % (width, height)
    lastReq = Visits.objects.filter(ip__exact=request.META['REMOTE_ADDR']).order_by('-datetime').all()[:1][0]
    if not lastReq.resolution:
        lastReq.resolution = res_string
        lastReq.save()

def getImage():
    image = PIL.Image.new('RGB', (163, 45), '#ffffff')
    font = PIL.ImageFont.truetype('uskovapp/Helvetica_Light-Normal.ttf', size=12, encoding='utf-8')
    draw = PIL.ImageDraw.Draw(image)
    draw.text((3,3), u'Всего: ' + unicode(len(getAllSessions())), fill='#000000', font=font)
    draw.text((3,18), u'Сегодня: ' + unicode(len(getTodaySessions())), fill='#000000', font=font)
    draw.text((3,33), u'Последний: ' + unicode(getLastSessionDatetime()), fill='#000000', font=font)
    string = StringIO.StringIO()
    image.save(string, 'PNG')
    return string.getvalue()


    