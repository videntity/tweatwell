from django.db import models

class Tip(models.Model):
    text         = models.TextField(max_length=1000)
    date         = models.DateField(auto_now_add=True)
    class Meta:
        ordering = ['-date']
    
    def __unicode__(self):
        return '%s ' % (self.text)



class CurrentTip(models.Model):
    tip          = models.ForeignKey(Tip)
    date         = models.DateField(auto_now_add=True)
    class Meta:
        ordering = ['-date']
    
    def __unicode__(self):
        return '%s ' % (self.tip)