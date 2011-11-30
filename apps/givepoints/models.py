from django.db import models
from django.contrib.auth.models import User
from ..upload.forms import uploadOMHE2restcat
from omhe.core.parseomhe import parseomhe
from tweatwell import settings
# Create your models here.

class GivePoints(models.Model):
    user  = models.ForeignKey(User)
    points = models.IntegerField()

    def save(self, *args, **kwargs):
        omhestr="pts=%s" % (self.points)
        o= parseomhe()
        d=o.parse(omhestr)
        r=uploadOMHE2restcat(d, settings.RESTCAT_USER, settings.RESTCAT_PASS,
                             self.user.email, settings.RESTCAT_USER_EMAIL,
                             self.user.email, 2)
        #super(GivePoints, self).save(*args, **kwargs)
    def __unicode__(self):
        return '%s points for %s|%s' % (self.points, self.user.username,
                                        self.user.email)
