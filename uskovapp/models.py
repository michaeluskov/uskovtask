from django.db import models

# Create your models here.


class Visits(models.Model):
    ip = models.GenericIPAddressField()
    url = models.CharField(max_length=200)
    datetime = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return "%s : %s (%s)" % (unicode(self.ip), unicode(self.datetime), 
                                 unicode(self.url))
