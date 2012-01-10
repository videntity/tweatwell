from django.db import models

class Tip(models.Model):
    text         = models.TextField(max_length=1000)
    date         = models.DateField(auto_now_add=True)
    class Meta:
        ordering = ['-date']
    
    def __unicode__(self):
        return '%s ' % (self.text)



class CurrentTip(models.Model):
    index        = models.IntegerField(max_length=4,default=0)
    
    def __unicode__(self):
        return '%s ' % (self.index)