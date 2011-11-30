from django.db import models
from django.contrib.auth.models import User

rank_choices=(
        ('1','1'), ('2','2'), ('3','3'), ('4','4'), ('5','5'),
        ('6','6'), ('7','7'), ('8','8'), ('9','9'), ('10','10'),
        )


class MaleCoachesPoll(models.Model):
    user  = models.ForeignKey(User, unique=True)
    rank = models.CharField(max_length=2, choices=rank_choices)
    comments = models.CharField(max_length=140, blank=True)
    
    class Meta:
        ordering = ('rank',)

    
    def __unicode__(self):
        return '%s is in %s place. Comments=%s' % (self.user.username,
       						self.rank,
       						self.comments)
class FemaleCoachesPoll(models.Model):
    user  = models.ForeignKey(User, unique=True)
    rank = models.CharField(max_length=2, choices=rank_choices)
    comments = models.CharField(max_length=140, blank=True)
    
    class Meta:
        ordering = ('rank',)
    
    def __unicode__(self):
        return '%s is in %s place. Comments=%s' % (self.user.username,
       						self.rank,
       						self.comments)
