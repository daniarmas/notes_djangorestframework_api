from django.contrib.auth.models import User
from rest_framework import serializers

from core.models import Note


class NoteSerializerForUser(serializers.Serializer):
    class Meta:
        model = Note
        exclude = ['delete_time']


class UserSerializer(serializers.ModelSerializer):
    notes = NoteSerializerForUser(many=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'notes']
