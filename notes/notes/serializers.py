from django.contrib.auth.models import User, Group
from rest_framework import serializers

from notes.notes.models import Label, Note


# class UserSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = User
#         fields = ['url', 'username', 'email', 'groups', 'notes']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = ['id', 'title']


class NoteSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(
        required=False, allow_blank=False, max_length=100)
    message = serializers.CharField(allow_blank=True, allow_null=True)
    owner = serializers.ReadOnlyField(source='owner.username')
    create_time = serializers.DateTimeField(required=False)
    delete_time = serializers.DateTimeField(required=False, allow_null=True)

    def create(self, validated_data):
        """
        Create and return a new `Note` instance, given the validated data.
        """
        return Group.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Note` instance, given the validated data.
        """
        instance.title = validated_data.get('title', instance.title)
        instance.message = validated_data.get('message', instance.message)
        instance.create_time = validated_data.get(
            'create_time', instance.create_time)
        instance.delete_time = validated_data.get(
            'delete_time', instance.delete_time)
        instance.save()
        return instance

    class Meta:
        model = Label
        fields = ['id', 'title']


class UserSerializer(serializers.ModelSerializer):
    notes = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Note.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'notes']
