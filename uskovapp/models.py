from django.db import models
from django.contrib.auth.models import User
from django.utils.html import escape
import re

# Create your models here.


class Sessions(models.Model):
    ip = models.GenericIPAddressField()
    datetime = models.DateTimeField(auto_now_add=True)
    
    
    def __unicode__(self):
            return "%s : %s" % (unicode(self.ip), 
                                unicode(self.datetime.strftime('%d/%m/%y %H:%M:%S')))    


class Visits(models.Model):
    session = models.ForeignKey(Sessions, null=True)
    ip = models.GenericIPAddressField()
    url = models.CharField(max_length=200)
    datetime = models.DateTimeField(auto_now_add=True)
    browser_name = models.CharField(max_length=200)
    browser_version = models.CharField(max_length=200)
    resolution = models.CharField(max_length=10, null=True, blank=True, default='')
    
    def __unicode__(self):
        return "%s : %s (%s)" % (unicode(self.ip), 
                                 unicode(self.datetime.strftime('%d/%m/%y %H:%M:%S')), 
                                 unicode(self.url))
    
    
class Comments(models.Model):
    user = models.ForeignKey(User)
    datetime = models.DateTimeField()
    
    def getActualCommentVersion(self):
        try:
            commentVersion = self.commentversions_set.all().order_by('-datetime')[:1][0]
            return commentVersion
        except Exception as e:
            return None
    
    
    def __unicode__(self):
        actualComment = self.getActualCommentVersion()
        return "%s: %s" % (self.user.username,
                           unicode(actualComment.text))
    
    
class CommentVersions(models.Model):
    comment = models.ForeignKey(Comments)
    datetime = models.DateTimeField()
    text = models.CharField(max_length=5000)
    
    def bbcode_parsed(self):
        text = escape(self.text)
        regex = re.compile(r'\[i](.*?)\[\/i]', re.MULTILINE)
        text = regex.sub('<i>\1</i>', text)
        regex = re.compile(r'\[b](.*?)\[\/b]', re.MULTILINE)
        text = regex.sub(r'<b>\1</b>', text)
        return text
       
    def __unicode__(self):
        return "%s %s %s" % (unicode(self.comment.user.username),
                             unicode(self.datetime.strftime('%d/%m/%y %H:%M:%S')),
                             unicode(self.text))