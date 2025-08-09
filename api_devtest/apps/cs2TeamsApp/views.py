from rest_framework import viewsets
from .models import Player
from django.shortcuts import render

# Create your views here.

class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    