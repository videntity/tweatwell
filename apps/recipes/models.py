from django.db import models
from django.conf import settings
from datetime import datetime
from django.contrib.auth.models import User
from sorl.thumbnail import ImageField


# Create your models here.
class Recipe(models.Model):
    name         = models.CharField(max_length=100)
    slug         = models.CharField(max_length=100)
    ingredients  = models.TextField(max_length=5000)
    detail       = models.TextField(max_length=10000)
    nutrition    = models.TextField(max_length=5000, blank=True, null=True)
    date         = models.DateField(auto_now_add=True)
    class Meta:
        ordering = ['-date']
    
    def __unicode__(self):
        return '%s ' % (self.name)

class RecipeComment(models.Model):
    user         = models.ForeignKey(User)
    recipe       = models.ForeignKey(Recipe)
    text         = models.CharField(max_length=100)
    points       = models.IntegerField(max_length=2, default=1)
    evdt         = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-evdt']
    
    def __unicode__(self):
        return 'Comment on %s by %s' % (self.recipe, self.user)