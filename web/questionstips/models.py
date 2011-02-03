from django.db import models

class QuestionTips(models.Model):
    question = models.CharField(max_length=500, blank=True)
    tip = models.CharField(max_length=500, blank=True)

    
    def __unicode__(self):
        return 'Question = %s . Tip=%s' % (self.question, self.tip)
