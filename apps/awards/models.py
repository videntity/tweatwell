from django.db import models
from django.contrib.auth.models import User
from ..upload.models import fruit_list, veg_list
award_choices=(
        ('President','President'), ('Dean','Dean'), ('Professor','Professor'),
        )
fvm=(('fruit', 'fruit'), ('veggie', 'veggie'), ('freggie', 'freggie'))
freggie_choices= fvm + fruit_list + veg_list

class Award(models.Model):
    user  = models.ForeignKey(User)
    award_class = models.CharField(max_length=15, choices=award_choices)
    freggie = models.CharField(max_length=40, choices=freggie_choices, blank=True)
    comments = models.CharField(max_length=140, blank=True)
    
    class Meta:
        ordering = ('freggie',)

    
    def __unicode__(self):
        return '%s is the %s of %s. Comments=%s' % (self.user.username,
       						self.award_class,
       						self.freggie,
                                                self.comments)
        
