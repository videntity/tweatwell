from django.db import models
from django.contrib.auth.models import User


class CurrentQuestion(models.Model):
    question_index = models.IntegerField(max_length=3, default=1)
    
    def __unicode__(self):
        return '%s' % (self.question_index)

class Question(models.Model):
    test = models.CharField(max_length=1024)
    
    def __unicode__(self):
        return '%s' % (self.test)

class Answer(models.Model):
    question = models.ForeignKey(Question)
    test = models.CharField(max_length=20)
    is_correct = models.BooleanField(default=False)
    
    def __unicode__(self):
        return '%s' % (self.test)
        
class CorrectAnswerPoints(models.Model):
    user    = models.ForeignKey(User)
    points  = models.IntegerField(max_length=2, default=5)
    evdate  = models.DateField(auto_now_add=True)
    
    
    def __unicode__(self):
        return '%s got %s on %s' % (self.user, self.points, self.evdate)