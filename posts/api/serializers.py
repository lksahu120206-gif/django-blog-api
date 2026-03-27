from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from posts.models import Post, Comment, Vote
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from posts.services.post_service import PostService
from posts.selectors.post_selectors import list_comments_for_post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.username', read_only=True)
    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    
    class Meta:
        model = Comment
        fields = ['id', 'content', 'author', 'created_at', 'post']
        read_only_fields = ['post']


class VoteSerializer(serializers.Serializer):
    vote = serializers.ChoiceField(choices=[1, -1])


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True, validators=[validate_password], min_length=8)
    new_password2 = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError("New passwords don't match")
        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password incorrect")
        return value


class PostSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.username', read_only=True)
    likes_count = serializers.SerializerMethodField()
    dislikes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    comments_preview = CommentSerializer(source='comment_list', many=True, read_only=True)
    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'content', 'author', 'likes_count', 
            'dislikes_count', 'comments_count', 'comments_preview', 'created_at'
        ]

    def get_likes_count(self, obj):
        return getattr(obj, 'likes_count', 0)

    def get_dislikes_count(self, obj):
        return getattr(obj, 'dislikes_count', 0)

    def get_comments_count(self, obj):
        return getattr(obj, 'comments_count', 0)


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password], min_length=8)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')
        extra_kwargs = {'email': {'required': True}}

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Passwords don't match."})
        if User.objects.filter(username=attrs['username']).exists():
            raise serializers.ValidationError({"username": "Username already taken."})
        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError({"email": "Email already registered."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        return User.objects.create_user(**validated_data)
