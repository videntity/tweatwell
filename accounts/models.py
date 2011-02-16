from django.db import models
from django.contrib.auth.models import User
from datetime import date

gender_choices=(
        ('female','female'),
        ('male','male'),
        )

class_choices=(
        ('freshman','freshman'),
        ('sophomore','sophomore'),
        ('junior','junior'),
        ('senior','senior'),
        ('graduate-level','graduate-level'),
        )

annon_choices=(
        ('Public','Public'),
        ('Anonymous','Anonymous'),
        )

award_choices=(
        ('President','President'),
        ('Dean','Dean'),
        ('Professor','Professor'),
        )


i=24
hc_list=[]
while i < 96:
     ft=i/12
     ft_in="%sft. %sin." %(i/12,i%12)
     choice=(i, ft_in)
     hc_list.append(choice)
     i=i+1
height_choices=tuple(hc_list)


class UserProfile(models.Model):
    user  = models.ForeignKey(User, unique=True)
    #display_name = models.CharField(max_length=30, blank=True)
    coach = models.BooleanField(default=False)
    studentid = models.CharField(max_length=20, blank=True)
    classlevel = models.CharField(max_length=15, choices=class_choices)
    gender = models.CharField(max_length=40, choices=gender_choices)
    pin = models.IntegerField(max_length=4, default=1234)
    birthdate = models.DateField(default=date.today())
    mobile_phone_number = models.CharField(max_length=15, blank=True)
    twitter = models.CharField(max_length=50, blank=True)
    steps_per_day_goal = models.IntegerField(max_length=7, default=10000, blank=True)
    annon = models.CharField(max_length=10, choices=annon_choices, default="Public")
    badge1 = models.BooleanField(default=False)
    badge2 = models.BooleanField(default=False)
    badge3 = models.BooleanField(default=False)
    badge4 = models.BooleanField(default=False)
    badge5 = models.BooleanField(default=False)
    veggie = models.CharField(max_length=10, choices=award_choices, blank=True)
    fruit =  models.CharField(max_length=10, choices=award_choices, blank=True)
    water =  models.CharField(max_length=10, choices=award_choices, blank=True)
    

    def __unicode__(self):
        return 'profile of %s' % self.user.username
