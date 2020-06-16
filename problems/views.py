# from django.shortcuts import render

from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Rule, Question
from .serializers import UserSerializer, QuestionSerializer, RuleSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class RuleViewSet(viewsets.ModelViewSet):
    queryset = Rule.objects.all()
    serializer_class = RuleSerializer
    permission_classes = [permissions.IsAuthenticated]


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=["get"])
    def question(self, request, *args, **kwargs):
        """ endpoint for getting a question

        detail is false becaues you can't ask for a question by pk
        """
        rule = Rule.objects.latest("pk")
        question = rule.question_from_rule()

        serializer = self.get_serializer(question)
        return Response(serializer.data)
