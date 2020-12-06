# from django.shortcuts import render

import random
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Rule, Calculation, Problem, FlashCard, Category
from .serializers import (
    UserSerializer,
    QuestionSerializer,
    RuleSerializer,
    CalculationSerializer,
    FlashCardSerializer,
    CategorySerializer,
)


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=["get"])
    def me(self, request):
        user = request.user
        print(request.user)

        serializer = self.get_serializer(user)
        return Response(serializer.data)


class RuleViewSet(viewsets.ModelViewSet):
    queryset = Rule.objects.all()
    serializer_class = RuleSerializer
    permission_classes = [permissions.IsAuthenticated]


class CalculationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Calculation.objects.all()
    serializer_class = CalculationSerializer
    permission_classes = [permissions.IsAuthenticated]


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

        # should make this read only somehow...
        serializer = self.get_serializer(problem)
        return Response(serializer.data)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FlashCardViewSet(viewsets.ModelViewSet):
    queryset = FlashCard.objects.none()
    serializer_class = FlashCardSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FlashCard.objects.filter(users=self.request.user)

    @action(detail=False, methods=["get"])
    def draw(self, request):
        # FlashCard.objects.filter
        qs = self.get_queryset()
        card_ids = qs.values_list("id", flat=True)
        card = random.choice(card_ids)
        serializer = self.get_serializer(qs.get(pk=card))
        return Response(serializer.data)
