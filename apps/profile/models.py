from django.db import models
from django.contrib.auth.models import User

QTY_CHOICES = ( (1,'1'), (2,'2'),(3,'3'), (4,'4'), (5,'5'),
                         (6,'6'), (7,'7'),(8,'8'), (9,'9'), (10,'10'))

class NonVeg(models.Model):
    nonveg  = models.CharField(max_length=140,
                verbose_name="Other food or beverage non-freggie")
    user    = models.ForeignKey(User)
    text    = models.CharField(max_length=140, blank=True, null=True,
                verbose_name="Say something about what else you're eating")
    quantity= models.IntegerField(max_length=2, default=1,
                                          choices=QTY_CHOICES)
    evdt    = models.DateTimeField(auto_now_add=True)
    evdate  = models.DateField(auto_now_add=True)
    evtz    = models.IntegerField(max_length=3, default=-5)
    txtz    = models.IntegerField(max_length=3, default=0)
    ttype   = models.CharField(max_length=10, default="txt")
    points  = models.IntegerField(max_length=3, default=0)
    
    class Meta:
        ordering = ['-evdt']
    
    def __unicode__(self):
        return '%s %s ate %s and said "%s" on %s' % (self.user.first_name,
                                        self.user.last_name, self.nonveg,
                                        self.text, self.evdt)
