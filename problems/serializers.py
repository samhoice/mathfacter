from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Rule, Question, Answer


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["url", "username", "email", "groups"]


class RuleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Rule
        fields = ["allowed_ops", "left", "right"]


class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Question
        fields = ["operation", "left_hand", "right_hand", "result"]
