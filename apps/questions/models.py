from django.db import models
from django.contrib.auth.models import User

class Question(models.Model):
    test = models.CharField(max_length=128)
    
    def __unicode__(self):
        return '%s' % (self.test)

class Answer(models.Model):
    question = models.ForeignKey(Question)
    test = models.CharField(max_length=20)
    is_correct = models.BooleanField(default=False)
    
    def __unicode__(self):
        return '%s' % (self.test)