from django.conf import settings
from django.db import models
from datetime import datetime
from utils import update_filename, save_to_restcat
from django.contrib.auth.models import User
from sorl.thumbnail import ImageField
import uuid

fruit_list=(
    ("apple", "Apple"),
    ("apricot", "Apricot"),
    ("avocado", "Avocado"),
    ("banana", "Banana"),
    ("blackberry", "Blackberry"),
    ("blueberry", "Blueberry"),
    ("cherry", "Cherry"),
    ("coconut", "Coconut"),
    ("crabapple", "Crabapple"),
    ("cranberry", "Cranberry"),
    ("grapefruit", "Grapefruit"),
    ("grapes", "Grapes"),
    ("keyLime", "KeyLime"),
    ("kiwi", "Kiwi"),
    ("lemon", "Lemon"),
    ("lime", "Lime"),
    ("mandarin", "Mandarin"),
    ("mango", "Mango"),
    ("melon", "Melon"),
    ("mulberry", "Mulberry"),
    ("nectarines", "Nectarines"),
    ("olive", "Olive"),
    ("orange", "Orange"),
    ("papaya", "Papaya"),
    ("passionfruit", "PassionFruit"),
    ("peach", "Peach"),
    ("pear", "Pear"),
    ("pineapple", "Pineapple"),
    ("plum", "Plum"),
    ("pomegranate", "Pomegranate"),
    ("paspberry", "Raspberry"),
    ("strawberry", "Strawberry"),
    ("tangerine", "Tangerine"),
    ("tomato", "Tomato"),
    ("watermelon", "Watermelon"),
    )

veg_list=(
    ("asparagus", "Asparagus"),
    ("beets", "Beets"),
    ("bell pepper", "BellPeppers"),
    ("broccoli", "Broccoli"),
    ("brussel sprouts", "Brussels Sprouts"),
    ("cabbage", "Cabbage"),
    ("carrots", "Carrots"),
    ("cauliflower", "Cauliflower"),
    ("celery", "Celery"),
    ("collard greens", "Collard greens"),
    ("corn", "Corn"),
    ("cucumbers", "Cucumbers"),
    ("eggplant", "Eggplant"),
    ("garlic", "Garlic"),
    ("green beans", "Green beans"),
    ("green peas", "Green peas"),
    ("kale", "Kale"),
    ("mushrooms", "Mushrooms"),
    ("okra", "Okra"),
    ("olives","Olives" ),
    ("onions", "Onions"),
    ("parsnips","Parsnips"),
    ("potatoes","Potatoes"),
    ("pumpkin", "Pumpkin"),
    ("romaine lettuce", "Romaine lettuce"),
    ("spinach", "Spinach"),
    ("squash", "Squash"),
    ("sweet potatoes","Sweet potatoes" ),
    ("turnip greens", "Turnip greens"),
    ("watercress","Watercress" ),
    ("yams", "Yams"),
    ("zucchini", "Zucchini"),
)


FREGGIE_CHOICES=tuple(list(fruit_list) + list(veg_list))


# Create your models here.
class Freggie(models.Model):
    sinceid         = models.CharField(max_length=20, null=True, blank=True)
    txid            = models.CharField(max_length=36, blank=True)
    user            = models.ForeignKey(User)
    file            = ImageField(upload_to=update_filename,
                       null=True, blank=True)
    freggie         = models.CharField(max_length=50, choices=FREGGIE_CHOICES)
    quantity        = models.IntegerField(max_length=1, default=1)
    note            = models.TextField(max_length=140, blank=True, null=True)
    evdt            = models.DateTimeField()
    txdt            = models.DateTimeField()
    evtz            = models.IntegerField(max_length=3, default=-5)
    txtz            = models.IntegerField(max_length=3, default=0)
    text            = models.CharField(max_length=140, blank=True)
    ttype           = models.CharField(max_length=10, default="omhe")
    points          = models.IntegerField(max_length=3, default=2)

    class Meta:
        ordering = ['-evdt']
    
    def __unicode__(self):
        return '%s ate %s (qty=%s) on %s' % (self.user, self.freggie,
                               self.quantity, self.evdt)    
    def save(self, **kwargs):
        self.txid=str(uuid.uuid4())
        profile=self.user.get_profile()
        now = datetime.utcnow()
        self.evdt=now#.strftime("%Y-%m-%d %H:%M:%S")
        self.txdt=now#.strftime("%Y-%m-%d %H:%M:%S")
        self.text="%s just ate %s" % (self.user, self.freggie )
        #                                     self.quantity,
        #                                     self.points)
        
        
        #result=save_to_restcat({'ttype': self.ttype,
        #                        'txid':self.txid,
        #                        'sndr': settings.RESTCAT_USER,
        #                        'rcvr': settings.RESTCAT_USER,
        #                        'subj': profile.anonymous_patient_id,
        #                        'evdt': self.evdt,
        #                        'txdt': self.txdt,
        #                        'evtz': self.evtz,
        #                        'txtz': self.txtz,
        #                        'sec': '2',
        #                        'text': self.text,
        #                        })
        #self.sinceid=str(uuid.uuid4())[0:20]
        super(Freggie, self).save(**kwargs)
        
class Comment(models.Model):
    freggie         = models.ForeignKey(Freggie, blank=True, null=True)
    sinceid         = models.CharField(max_length=20, blank=True, null=True)
    txid            = models.CharField(max_length=36, blank=True)
    user            = models.ForeignKey(User)
    text            = models.TextField(max_length=140)
    evdt            = models.DateTimeField(auto_now_add=True)
    txdt            = models.DateTimeField(auto_now_add=True)
    evtz            = models.IntegerField(max_length=3, default=-5)
    txtz            = models.IntegerField(max_length=3, default=0)
    ttype           = models.CharField(max_length=10, default="txt")
    points          = models.IntegerField(max_length=3, default=1)
    
    class Meta:
        ordering = ['evdt']
    
    def __unicode__(self):
        return '%s said: "%s"  on %s' % (self.user, self.text, self.evdt)
    
    def save(self, **kwargs):
        super(Comment, self).save(**kwargs)        
