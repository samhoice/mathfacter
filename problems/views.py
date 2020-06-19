# from django.shortcuts import render

from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Rule, Calculation, Problem
from .serializers import (
    UserSerializer,
    QuestionSerializer,
    RuleSerializer,
    CalculationSerializer,
)


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


class CalculationViewSet(viewsets.ModelViewSet):
    queryset = Calculation.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=["get"])
    def problem(self, request, *args, **kwargs):
        """ endpoint for getting a question

        """
        user = request.user

        session = user.mathsession_set.latest("created")
        rule = session.rules.latest("created")
        calculation = rule.question_from_rule()
        problem = Problem.objects.create(user=request.user, calculation=calculation)

        serializer = self.get_serializer(problem)
        return Response(serializer.data)


class ProblemViewSet(viewsets.ModelViewSet):
    queryset = Problem.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Problem.objects.filter(user=self.request.user)

    def list(self, request):
        user = request.user

        session = user.mathsession_set.latest("created")
        rule = session.rules.latest("created")
        calculation = rule.question_from_rule()
        problem = Problem.objects.create(user=request.user, calculation=calculation)

        serializer = self.get_serializer(problem)
        return Response(serializer.data)
