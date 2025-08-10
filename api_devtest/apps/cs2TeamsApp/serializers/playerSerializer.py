from ..models import Player
from rest_framework import serializers, viewsets

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = "__all__"