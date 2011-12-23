from django.db import models
from django.contrib.auth.models import User
from datetime import date, timedelta
class Roulette(models.Model):
    user            = models.ForeignKey(User)
    points          = models.IntegerField(max_length=3, default=0)
    date            = models.DateField(auto_now_add=True)
    
    class Meta:
        ordering = ['date']
        get_latest_by = "date"
        unique_together = (("user", "date"),)  
    
    def __unicode__(self):
        return '%s got %s points via roulette on %s' % (self.user, self.points,
                                                        self.date)

def last_spin_date(user):
    try:
        r=Roulette.objects.filter(user=user).latest()
        return r.date
    except(IndexError):
        return date.today() - timedelta(1)
    except(Roulette.DoesNotExist):
        return date.today() - timedelta(1)        

def can_spin(user):
    try:
        r=Roulette.objects.filter(user=user).latest()
        if r.date == date.today():
            return False
    except(IndexError):
        return True
    except(Roulette.DoesNotExist):
        return True
    return True