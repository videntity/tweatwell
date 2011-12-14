from django.db import models
from django.contrib.auth.models import User


class QuestionAnswerChoices(models.Model):
    choice = models.CharField(max_length=100)
    def __unicode__(self):
        return '%s' % (self.choice)


class Question(models.Model):
    question       = models.CharField(max_length=500)
    answer         = models.CharField(max_length=100)
    answer_choices = models.ManyToManyField(QuestionAnswerChoices)
    display        = models.BooleanField()
    
    def __unicode__(self):
        return 'Display=%s, Question = %s, Answer=%s' % (self.display,
                                                         self.question,
                                                         self.answer)


class QuestionAnswer(models.Model):
    question        = models.ForeignKey(Question)
    user            = models.ForeignKey(User)
    answer          = models.CharField(max_length=100)
    correct         = models.BooleanField()
    created_on      = models.DateField(auto_now_add=True)
    
    class Meta:
        unique_together = (("question", "user"),)
        ordering = ('-created_on',)
        get_latest_by = "created_on"
    
    def __unicode__(self):
        if self.correct==True:
            return '%s got it right on %s.' % (self.user, self.created_on)
        return '%s got it wrong on %s.' % (self.user, self.created_on)
        
    def save(self, **kwargs):
        
        if self.question.answer==self.answer:
            self.correct=True
        
        super(QuestionAnswer, self).save(**kwargs)