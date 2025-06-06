import datetime

from django.db import models
from django.utils import timezone

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")

    def __str__(self):
      return self.question_text
  
    def was_published_recently(self):
      return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
      return self.choice_text


class Category(models.Model):
    topic = models.CharField(max_length=200)
    timestamp = models.IntegerField(default=100)
    neighbour_node = models.CharField(max_length=200, default="")
    neighbour_node_weight = models.FloatField(default=0)


class Info(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    info = models.CharField(max_length=200)