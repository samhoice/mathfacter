from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Rule, Calculation, Problem


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["url", "username", "email", "groups"]


class RuleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Rule
        fields = ["allowed_ops", "left", "right"]


class CalculationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Calculation
        fields = ["operation", "left_hand", "right_hand", "result"]


class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    calculation = CalculationSerializer(read_only=True)

    class Meta:
        model = Problem
        fields = ["calculation", "value", "correct", "answered"]
        read_only_fields = ["correct", "answered"]

    def update(self, instance, validated_data):
        if instance.answered:
            # TODO Error
            return instance

        instance.value = validated_data.get("value", instance.value)
        if instance.value == instance.calculation.result:
            instance.correct = True

        instance.answered = True
        instance.save()

        return instance
