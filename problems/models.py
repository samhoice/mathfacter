from django.db import models
from django.contrib.auth.models import User
import random


class Rule(models.Model):
    # for brevity, min is 0
    allowed_ops = models.CharField(max_length=4)

    left = models.IntegerField()
    left_exact = models.BooleanField()
    right = models.IntegerField()
    right_exact = models.BooleanField()

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} {} {}".format(self.left, self.allowed_ops, self.right)

    def question_from_rule(self):
        left = random.randint(0, self.left)
        right = random.randint(0, self.right)
        op = random.choice(self.allowed_ops)

        q = Calculation.objects.get_or_create(
            rule=self, operation=op, left_hand=left, right_hand=right
        )

        q[0].calculate()

        return q[0]


class Calculation(models.Model):
    rule = models.ForeignKey(
        Rule, null=True, default=None, blank=True, on_delete=models.CASCADE
    )
    created = models.DateTimeField(auto_now_add=True)
    operation = models.CharField(max_length=1)
    left_hand = models.IntegerField()
    right_hand = models.IntegerField()
    result = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return "{} {} {}".format(self.left_hand, self.operation, self.right_hand)

    def calculate(self):
        if self.operation == "+":
            self.result = self.left_hand + self.right_hand
        elif self.operation == "-":
            self.result = self.left_hand - self.right_hand
        elif self.operation == "*":
            self.result = self.left_hand * self.right_hand
        elif self.operation == "/":
            if self.right_hand == 0:
                # don't change
                return
            else:
                self.result = self.left_hand / self.right_hand

        self.save()


class Problem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    calculation = models.ForeignKey(Calculation, on_delete=models.CASCADE)
    value = models.IntegerField(default=0)
    correct = models.BooleanField(default=False)
    answered = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}".format(self.value)


class MathSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rules = models.ManyToManyField(Rule)

    created = models.DateTimeField(auto_now_add=True)
    ended = models.DateTimeField(null=True, default=None, blank=True)

    def __str__(self):
        return "{}'s session with {} rule(s)".format(
            self.user.first_name, self.rules.count()
        )
