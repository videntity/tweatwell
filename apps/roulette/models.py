from django.db import models
from django.contrib.auth.models import User

class Roulette(models.Model):
    user            = models.ForeignKey(User)
    points          = models.IntegerField(max_length=3, default=0)
    date            = models.DateField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date']
    
    def __unicode__(self):
        return '%s got %s points via roulette on %s' % (self.user, self.points,
                                                        self.date)

