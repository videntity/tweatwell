from django.db import models
from django.contrib.auth.models import User

class NonVeg(models.Model):
    nonveg  = models.CharField(max_length=140,
                verbose_name="Other food or beverage non-freggie")
    user    = models.ForeignKey(User)
    text    = models.CharField(max_length=140, blank=True, null=True,
                verbose_name="Say something about what else you're eating")
    evdt    = models.DateTimeField(auto_now_add=True)
    evdate  = models.DateField(auto_now_add=True)
    evtz    = models.IntegerField(max_length=3, default=-5)
    txtz    = models.IntegerField(max_length=3, default=0)
    ttype   = models.CharField(max_length=10, default="txt")
    points  = models.IntegerField(max_length=3, default=0)
    
    class Meta:
        ordering = ['-evdt']
    
    def __unicode__(self):
        return '%s ate %s and said "%s" on %s' % (self.user, self.nonveg,
                                                   self.text, self.evdt)
