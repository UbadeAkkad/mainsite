from rest_framework import serializers
from django.contrib.auth.models import User
from notes.models import Note
from todo.models import Task 
from quiz.models import Quiz


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(username = validated_data['username'], password = validated_data['password'])

        return user
    
class GuestUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','password')

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ("id","title","body","color","created")

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ("id","title","description","complete")

class Quizserializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ("name","quiz_ID","created")

class QuizPageserializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ("name",)