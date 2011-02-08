from django.db import models
from django.contrib.auth.models import User


class FoodReport(models.Model):
    user  =     models.ForeignKey(User, unique=True)
    fruits =    models.IntegerField(default=0)
    veggies =   models.IntegerField(default=0)
    water =     models.IntegerField(default=0)
    answers =   models.IntegerField(default=0)
    alcohol =   models.IntegerField(default=0)
    points =    models.IntegerField(default=0)
    
    class Meta:
        ordering = ('points',)

    
    def __unicode__(self):
        return '%s %s has %s points' % (self.user.username,
       						self.user.email,
       						self.points)
class UserStatusReport(models.Model):
    user  =     models.ForeignKey(User)
    status =    models.CharField(max_length=140)
    
    def __unicode__(self):
        return '%s  - %s' % (self.user.username, self.status)