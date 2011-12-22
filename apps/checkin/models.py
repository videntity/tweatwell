from django.conf import settings
from django.db import models
from datetime import datetime, timedelta, date
from utils import update_filename, save_to_restcat
from django.contrib.auth.models import User
from sorl.thumbnail import ImageField
import uuid
from freggies import fruit_choices, fruit_tuple, veg_choices, veg_tuple

FOV_CHOICES = (('fruit', 'fruit'),('veg','veg'))
FREGGIE_CHOICES=tuple(list(fruit_choices) + list(veg_choices))


class FreggieGoal(models.Model):
    user            = models.ForeignKey(User)
    evdate          = models.DateField(auto_now_add=True)
    freggie_goal    = models.IntegerField(max_length=2)
    
    def __unicode__(self):
        return "%s's goal was %s on %s" % (self.user, self.freggie_goal,
                             self.evdate) 
    def save(self, **kwargs):
        super(FreggieGoal, self).save(**kwargs)

# Create your models here.
class Freggie(models.Model):
    sinceid         = models.CharField(max_length=20, null=True, blank=True)
    txid            = models.CharField(max_length=36, blank=True)
    user            = models.ForeignKey(User)
    photo           = ImageField(upload_to=update_filename, null=True, blank=True,
                       verbose_name="Upload a photo of your freggie for 5 extra points.")
    freggie         = models.CharField(max_length=50, choices=FREGGIE_CHOICES)
    freggie_other   = models.CharField(max_length=50, blank=True, null=True)
    fruit_or_veg    = models.CharField(max_length=5, choices=FOV_CHOICES,
                                       blank=True, null=True)
    quantity        = models.IntegerField(max_length=1, default=1)
    note            = models.TextField(max_length=140, blank=True, null=True)
    evdate          = models.DateField(auto_now_add=True)
    evdt            = models.DateTimeField(blank=True)
    evtz            = models.IntegerField(max_length=3, default=-5)
    txtz            = models.IntegerField(max_length=3, default=0)
    text            = models.CharField(max_length=140, blank=True, null=True,
                                verbose_name="Say something about your freggie")
    eattext         = models.CharField(max_length=140, blank=True)
    ttype           = models.CharField(max_length=10, default="omhe")
    points          = models.IntegerField(max_length=3, default=2)
    class Meta:
        ordering = ['-evdt']
    
    def __unicode__(self):
        return '%s ate %s (qty=%s) on %s' % (self.user, self.freggie,
                               self.quantity, self.evdt)    
    def save(self, **kwargs):
        self.txid=str(uuid.uuid4())
        #profile=self.user.get_profile()
        now = datetime.now()
        if self.evdt:
            #assuming we are getting this from twitter which reports in UTC time.
            #adjust accordingly.
            self.evdt=self.evdt + timedelta(hours=settings.TIMEZONE_OFFSET)
        else:
            self.evdt=now
            
        if self.quantity > 1:
            self.points=self.points * self.quantity
        
        if self.photo:
            self.points=self.points+5
        
        if fruit_tuple.__contains__(self.freggie):
            self.fruit_or_veg="fruit"
        else:
            self.fruit_or_veg="veg"
            
        if self.freggie=="other_fruit" or self.freggie=="other_veg":
            self.freggie=self.freggie_other
        
        self.eattext=" %s just ate %s" % (self.user, self.freggie )
        
        try:
            f=FreggieGoal.objects.get(user=self.user, evdate=date.today())
            f.freggie_goal=self.user.get_profile().daily_freggie_goal
            f.save()
        except(FreggieGoal.DoesNotExist):
            FreggieGoal.objects.create(user=self.user,
                    freggie_goal=self.user.get_profile().daily_freggie_goal )
        
        super(Freggie, self).save(**kwargs)



class Comment(models.Model):
    freggie         = models.ForeignKey(Freggie, blank=True, null=True)
    sinceid         = models.CharField(max_length=20, blank=True, null=True)
    txid            = models.CharField(max_length=36, blank=True)
    user            = models.ForeignKey(User)
    text            = models.TextField(max_length=140)
    evdt            = models.DateTimeField(auto_now_add=True)
    txdt            = models.DateTimeField(auto_now_add=True)
    evtz            = models.IntegerField(max_length=3, default=-5)
    txtz            = models.IntegerField(max_length=3, default=0)
    ttype           = models.CharField(max_length=10, default="txt")
    points          = models.IntegerField(max_length=3, default=1)
    
    class Meta:
        ordering = ['evdt']
    
    def __unicode__(self):
        return '%s said: "%s"  on %s' % (self.user, self.text, self.evdt)
    
    def save(self, **kwargs):
        super(Comment, self).save(**kwargs)
        
        
BADGE_CHOICES=(('fruitdean','fruitdean'),('vegdean','vegdean'),
                ('president','president'),('professor','professor'))

class BadgePoints(models.Model):
    user            = models.ForeignKey(User)
    badge           = models.CharField(max_length=20, choices=BADGE_CHOICES)
    evdate            = models.DateField(auto_now_add=True)
    points          = models.IntegerField(max_length=2, default=0)
    class Meta:
        ordering = ['-evdate']
    
    def __unicode__(self):
        return '%s got the %s badge and %s points on %s' % (self.user,
                                self.badge, self.evdate, self.points)
    
    def save(self, **kwargs):
        if self.badge=="president":
            self.points=5
        if self.badge=="fruitdean" or self.badge=="vegdean":
            self.points=3
        if self.badge=="professor":
            self.points=1
        super(BadgePoints, self).save(**kwargs)