from rest_framework import serializers
from ..models import Type_Player

class TypePlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type_Player
        fields = "__all__"