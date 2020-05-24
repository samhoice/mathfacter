from django.db import models
import random


class Rule(models.Model):
    # for brevity, min is 0
    allowed_ops = models.CharField(max_length=4)
    left = models.IntegerField()
    right = models.IntegerField()

    def question_from_rule(self):
        left = random.randint(0, self.left)
        right = random.randint(0, self.right)

        q = Question.object.get_or_create(
            rule=self, operation=self.op, left_hand=left, right_hand=right
        )
        q.calculate()

        return q


class Question(models.Model):
    rule = models.ForeignKey(
        Rule, null=True, default=None, blank=True, on_delete=models.CASCADE
    )
    created = models.DateTimeField(auto_now_add=True)
    operation = models.CharField(max_length=1)
    left_hand = models.IntegerField()
    right_hand = models.IntegerField()
    result = models.IntegerField(null=True, blank=True)

    def calculate(self):
        if self.operation == "+":
            self.result = self.left_hand + self.right_hand
        elif self.operation == "-":
            self.result = self.left_hand - self.right_hand
        elif self.operation == "*":
            self.result = self.left_hand * self.right_hand
        elif self.operation == "/":
            self.result = self.left_hand / self.right_hand


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    value = models.IntegerField()
    correct = models.BooleanField(default=False)
