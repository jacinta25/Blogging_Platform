from rest_framework import serializers
from .models import User, BlogPost

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class BlogPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'content', 'category', 'author', 'publish_date', 'created_at', 'updated_at']
