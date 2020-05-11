from django.db import models


class Rule(models.Model):
    pass


class Question(models.Model):
    rule = models.ForeignKey(Rule, null=True, default=None, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    operation = models.CharField(max_length=8)
    left_hand = models.IntegerField()
    right_hand = models.IntegerField()


class Answer(models.Model):
    question = models.ForeignKey(Question)
    value = models.IntegerField()
