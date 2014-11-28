from django.db import models

# Create your models here.


class Visits(models.Model):
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
