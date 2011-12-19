from django.db import models
from datetime import datetime
from django.contrib.auth.models import User


"""The score required to pass the quiz."""
MIN_QUIZ_PASS_SCORE=100

"""The number of random questions to be be asked.
The total number of questions is this number + all required questions.
""" 
QUIZ_NUM_RAND_QUESTIONS=0


class Category(models.Model):
    """defines both the question and quiz category. gr, video, graphic design, etc"""
    name  = models.CharField(max_length=200, unique=True)
    slug  = models.SlugField(max_length=100, unique=True)
    
    def __unicode__(self):
        return self.name
    

class Question(models.Model):
    """An individual question. Answer choice are in the Answer model"""
    category            = models.ManyToManyField(Category)
    name                = models.CharField(max_length=200, unique=True)
    slug                = models.SlugField(max_length=100, unique=True)
    question_text       = models.TextField(max_length=500)
    explanation         = models.TextField(max_length=500)
    always_ask          = models.BooleanField(default=False)
    must_get_right      = models.BooleanField(default=False)
    created_at          = models.DateTimeField(default=datetime.utcnow)
    
    class Meta:
        ordering = ('-created_at',)

    def __unicode__(self):
        return "%s: AlwaysAsk=%s,  MustGetRight=%s" % (self.slug,
                                                       self.always_ask,
                                                       self.must_get_right,)

class Answer(models.Model):
    """A possible answer choice for a particlar question. either correct or incorrect."""
    question    = models.ForeignKey(Question)
    answer      = models.CharField(max_length=20)
    correct     = models.BooleanField()

    def __unicode__(self):
        if self.correct==True:
            self.c="CORRECT"
        else:
            self.c="INCORRECT"
        return "%s is the %s answer to %s" % (self.answer, self.c, self.question.slug)



class Quiz(models.Model):
    """An individual quiz made up of req. & random ?'s. (via Response model)"""
    category    = models.ForeignKey(Category)
    question    = models.ManyToManyField(Question, blank=True, through='Response')
    user        = models.ForeignKey(User)
    attempt     = models.IntegerField(default=0)
    passed      = models.BooleanField(default=False)
    score       = models.IntegerField(default=-1)
    created_at  = models.DateTimeField(default=datetime.utcnow)
     
    def __unicode__(self): 
        return "%s: Quiztype %s for %s %s. Score=%s Passed=%s" % (self.id,
                                                  self.category.name,
                                                  self.user.first_name,
                                                  self.user.last_name,
                                                  self.score,
                                                  self.passed)
    class Meta:
        ordering = ('-created_at',)
        get_latest_by = "created_at"



class Response(models.Model):
    """A particular user response to a prarticular question for a particular quiz."""
    """Via Quiz, Question, and Answer models."""
    quiz        = models.ForeignKey(Quiz)
    question    = models.ForeignKey(Question)
    answer      = models.ForeignKey(Answer, blank=True, null=True)
    correct     = models.BooleanField(default=False)
    created_at  = models.DateTimeField(default=datetime.utcnow)
    
    def __unicode__(self):
        return "Quiz=%s, User=%s %s,  Question=%s, Correct=%s" % (
                                                  self.quiz.id,
                                                  self.quiz.user.first_name,
                                                  self.quiz.user.last_name,
                                                  self.question.slug,
                                                  self.correct)
