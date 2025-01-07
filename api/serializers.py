from rest_framework import serializers
from django.contrib.auth import get_user_model
from blog.models import (
    BlogPost,
    Category,
    Tag,
    Comment,
    PostLike,
    PostRating,
    AuthorSubscription,
    Notification
)

#Get the User model for authentication and user data handling
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['id','username', 'email', 'bio', 'profile_picture']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']
        
class BlogPostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True) #nested serializer for author details
    category = CategorySerializer(read_only=True)#nested serializer for category
    tags = TagSerializer(many=True, read_only=True)
    comments = serializers.StringRelatedField(many=True, read_only=True)# Related comments
    content_as_html = serializers.ReadOnlyField()# HTML-rendered content
     
    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'content', 'author', 'category', 'published_date', 'created_date', 'tags', 'comments', 'content_as_html']
    
    # validates the title field to ensure it's not empty
    def validate_title(self, value):
        if not value:
            raise serializers.ValidationError("Title is required.")
        return value
    
    # validates content field to ensure its not empty 
    def validate_content(self, value):
        if not value:
            raise serializers.ValidationError("Content is required.")
        return value
    
    #validates the author field to ensure it's not empty
    def validate_author(self, value):
        if not value:
            raise serializers.ValidationError("Author is required.")
        return value
    

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'content', 'created_date']

class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLike
        fields = ['user', 'post', 'created_at']

class PostRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostRating
        fields = ['user', 'post', 'rating', 'created_at']

class AuthorSubscriptionSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)# Nested serializer for author details

    class Meta:
        model = AuthorSubscription
        fields = ['user', 'author', 'subscribed_at']


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'user', 'message', 'create_at', 'is_read']

