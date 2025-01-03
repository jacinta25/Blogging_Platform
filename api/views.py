from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied, NotFound, ValidationError
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth import get_user_model
from django.db.models import Prefetch
from blog.models import BlogPost, Category, Tag, Comment, PostLike, PostRating, AuthorSubscription 
from .serializers import BlogPostSerializer, CategorySerializer, TagSerializer, UserSerializer, CommentSerializer
from .filters import BlogPostFilter
from .permissions import IsOwnerOrReadOnly
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from django.db import models
from django.core.mail import send_mail

User = get_user_model()


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def subscribe(self, request, pk=None):
        author = self.get_object()
        if AuthorSubscription.objects.filter(user=request.user, author=author).exists():
            return Response({"detail": "Already subscribed to this author."}, status=status.HTTP_400_BAD_REQUEST)
        AuthorSubscription.objects.create(user=request.user, author=author)
        return Response({"detail": "Successfully subscribed to the author."}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['delete'], permission_classes=[IsAuthenticated])
    def unsubscribe(self, request, pk=None):
        author = self.get_object()
        subscription = AuthorSubscription.objects.filter(user=request.user, author=author).first()
        if not subscription:
            return Response({"detail": "You are not subscribed to this author."}, status=status.HTTP_400_BAD_REQUEST)
        subscription.delete()
        return Response({"detail": "Successfully unsubscribed from the author."}, status=status.HTTP_204_NO_CONTENT)

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
    
 


    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def like_post(self, request, pk=None):
        post = self.get_object()
        if PostLike.objects.filter(user=request.user, post=post).exists():
            return Response({"detail": "You already liked this post."}, status=status.HTTP_400_BAD_REQUEST)
        PostLike.objects.create(user=request.user, post=post)
        return Response({"detail": "Post liked successfully."}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def rate_post(self, request, pk=None):
        post = self.get_object()
        rating_value = request.data.get('rating')
        if not rating_value or not (1 <= int(rating_value) <= 5):
            return Response({"detail": "Rating must be between 1 and 5."}, status=status.HTTP_400_BAD_REQUEST)
        rating, created = PostRating.objects.update_or_create(
            user=request.user, post=post, defaults={'rating': rating_value})
        return Response({"detail": f"Post rated successfully with {rating_value}."}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def most_liked(self, request):
        most_liked_posts = BlogPost.objects.annotate(likes_count=models.Count('postlike')).order_by('-likes_count')
        serializer = BlogPostSerializer(most_liked_posts, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def highest_rated(self, request):
        highest_rated_posts = BlogPost.objects.annotate(average_rating=models.Avg('postrating__rating')).order_by('-average_rating')
        serializer = BlogPostSerializer(highest_rated_posts, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def share_post(self, request, pk=None):
        post = self.get_object()
        email = request.data.get('email')

        if not email:
            return Response({"detail": "Email is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            send_mail(
                subject=f"Check out this blog post: {post.title}",
                message=post.content,
                from_email='no-reply@blog.com',
                recipient_list=[email],
            )
            return Response({"detail": "Post shared successfully."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
 

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


