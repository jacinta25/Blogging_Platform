from rest_framework import serializers
from django.contrib.auth import get_user_model
from blog.models import BlogPost, Category, Tag, Comment, PostLike, PostRating, AuthorSubscription

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
    comments = serializers.StringRelatedField(many=True, read_only=True)
    tags = TagSerializer(many=True, required=False, read_only=True)

    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'content', 'author', 'category', 'published_date', 'created_date', 'tags', 'comments']
    
    def validate_title(self, value):
        if not value:
            raise serializers.ValidationError("Title is required.")
        return value
    
    def validate_content(self, value):
        if not value:
            raise serializers.ValidationError("Content is required.")
        return value
    def validate_author(self, value):
        if not value:
            raise serializers.Validationerror("Author is required.")
        return value
    

class CommentSerializer():
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
    