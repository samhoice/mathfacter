from django.db import models
from django.contrib.auth.models import User
import random


class Rule(models.Model):
    """ Represents a way of generating math problems for a user

    Minimum and maximum values, plus the allowed operations to apply
    to generate a math fact.

    If flip is set, the problems generated will have the option to
    randomly swap the operands.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=128, default="")

    allowed_ops = models.CharField(max_length=4)

    left = models.IntegerField()
    left_min = models.IntegerField(default=0)
    right = models.IntegerField()
    right_min = models.IntegerField(default=0)
    flip = models.BooleanField(default=True)

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} {} {}".format(self.left, self.allowed_ops, self.right)

    def question_from_rule(self):
        left = random.randint(self.left_min, self.left)
        right = random.randint(self.right_min, self.right)
        op = random.choice(self.allowed_ops)

        if self.flip:
            if random.choice([True, False]):
                left, right = right, left

        q = Calculation.objects.get_or_create(
            rule=self, operation=op, left_hand=left, right_hand=right
        )

        q[0].calculate()

        return q[0]


class Calculation(models.Model):
    """ Represents a problem generated from a rule. This is the problem
    to be solved
    """

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
    """ This is the user's calculation. It links to a 'calculation'
    and has the user's answer.

    This and calculation should probably swap names

    """

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


class Category(models.Model):
    """ represents the category for a text/image based flashcard

    Will need to allow you to only look at a single category.
    """

    name = models.CharField(max_length=64)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class FlashCard(models.Model):
    """ Represents a text based flashcard for memorization.

    Model for a generic flashcard with text on the front and back, that doesn't
    have a solvable math fact on it. Useful for memorizing things.

    There's currently no facility for checking these. just for memorizing
    """

    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    users = models.ManyToManyField(User)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    front_text = models.TextField()
    back_text = models.TextField()

    def __str__(self):
        return f"{self.front_text}"

    def user_str(self):
        return ", ".join([u.__str__() for u in self.users.all()[0:3]])
