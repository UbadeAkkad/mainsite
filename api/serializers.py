from rest_framework import serializers
from django.contrib.auth.models import User
from notes.models import Note
from todo.models import Task 


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])

        return user

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ("id","title","body","color")

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ("id","title","description","complete")