from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied, NotFound, ValidationError
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth import get_user_model
from django.db.models import Prefetch
from blog.models import BlogPost, Category, Tag, Comment
from .serializers import BlogPostSerializer, CategorySerializer, TagSerializer, UserSerializer, CommentSerializer
from .filters import BlogPostFilter
from .permissions import IsOwnerOrReadOnly
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

User = get_user_model()


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class BlogPostViewSet(ModelViewSet):
    queryset = BlogPost.objects.all().select_related('author', 'category')  # Optimize with select_related for related fields
    serializer_class = BlogPostSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = BlogPostFilter
    filterset_fields = ['category', 'author', 'status', 'published_date']
    search_fields = ['title', 'content', 'tags__name', 'author__username']
    ordering_fields = ['published_date', 'title']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied("You cannot update another user's post.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied("You cannot delete another user's post.")
        instance.delete()

    @action(detail=False, methods=['get'], url_path='category/(?P<category_name>[^/.]+)')
    def posts_by_category(self, request, category_name=None):
        if not category_name:
            raise ValidationError("Category name is required.")
        try:
            category = Category.objects.get(name=category_name)
        except Category.DoesNotExist:
            raise NotFound("Category not found.")
        
        # Prefetch related posts to optimize query
        posts = BlogPost.objects.filter(category=category).select_related('author').prefetch_related('tags')
        serializer = BlogPostSerializer(posts, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='author/(?P<author_username>[^/.]+)')
    def posts_by_author(self, request, author_username=None):
        if not author_username:
            raise ValidationError("Author username is required.")
        try:
            author = User.objects.get(username=author_username)
        except User.DoesNotExist:
            raise NotFound("Author not found.")
        
        posts = BlogPost.objects.filter(author=author).select_related('category').prefetch_related('tags')
        serializer = BlogPostSerializer(posts, many=True)
        return Response(serializer.data)

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]  # Optional: Only allow authenticated users to create/edit tags.

class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all().select_related('author', 'post')  # Optimize with select_related
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied("You cannot update another user's comment.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied("You cannot delete another user's comment.")
        instance.delete()
