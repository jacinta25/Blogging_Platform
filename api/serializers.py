from rest_framework import serializers
from django.contrib.auth import get_user_model
from blog.models import BlogPost, Category, Tag

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username', 'email']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']
        
class BlogPostSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'content', 'author', 'category', 'published_date', 'created_date', 'tags']
    