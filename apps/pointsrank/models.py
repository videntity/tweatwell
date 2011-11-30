from django.db import models
from django.contrib.auth.models import User


class PointsRank(models.Model):
    user  = models.ForeignKey(User, unique=True)
    points = models.IntegerField(blank=True)
    rank = models.IntegerField()
    comments = models.CharField(max_length=140, blank=True)
    
    class Meta:
        ordering = ('rank',)
    
    def __unicode__(self):
        return '%s is in %s place. Comments=%s' % (self.user.username,
       						   self.rank,
       						   self.comments)
