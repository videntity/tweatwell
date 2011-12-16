from django.conf import settings
from django.db import models
from datetime import datetime
from utils import update_filename, save_to_restcat
from django.contrib.auth.models import User
from sorl.thumbnail import ImageField
import uuid
from freggies import fruit_choices, fruit_tuple, veg_choices, veg_tuple

FOV_CHOICES = (('fruit', 'fruit'),('veg','veg'))
FREGGIE_CHOICES=tuple(list(fruit_choices) + list(veg_choices))


# Create your models here.
class Freggie(models.Model):
    sinceid         = models.CharField(max_length=20, null=True, blank=True)
    txid            = models.CharField(max_length=36, blank=True)
    user            = models.ForeignKey(User)
    photo           = ImageField(upload_to=update_filename,
                       null=True, blank=True)
    freggie         = models.CharField(max_length=50, choices=FREGGIE_CHOICES)
    freggie_other   = models.CharField(max_length=50, blank=True, null=True)
    fruit_or_veg    = models.CharField(max_length=5, choices=FOV_CHOICES,
                                       blank=True, null=True)
    quantity        = models.IntegerField(max_length=1, default=1)
    note            = models.TextField(max_length=140, blank=True, null=True)
    evdt            = models.DateTimeField()
    txdt            = models.DateTimeField()
    date            = models.DateField(auto_now_add=True)
    timestamp       = models.DateTimeField(auto_now_add=True)
    evtz            = models.IntegerField(max_length=3, default=-5)
    txtz            = models.IntegerField(max_length=3, default=0)
    text            = models.CharField(max_length=140, blank=True, null=True)
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
        now = datetime.utcnow()
        self.evdt=now#.strftime("%Y-%m-%d %H:%M:%S")
        self.txdt=now#.strftime("%Y-%m-%d %H:%M:%S")
        self.eattext=" %s just ate %s" % (self.user, self.freggie )
        if fruit_tuple.__contains__(self.freggie):
            self.fruit_or_veg="fruit"
        else:
            self.fruit_or_veg="veg"
        #result=save_to_restcat({'ttype': self.ttype,
        #                        'txid':self.txid,
        #                        'sndr': settings.RESTCAT_USER,
        #                        'rcvr': settings.RESTCAT_USER,
        #                        'subj': profile.anonymous_patient_id,
        #                        'evdt': self.evdt,
        #                        'txdt': self.txdt,
        #                        'evtz': self.evtz,
        #                        'txtz': self.txtz,
        #                        'sec': '2',
        #                        'text': self.text,
        #                        })
        #self.sinceid=str(uuid.uuid4())[0:20]
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
