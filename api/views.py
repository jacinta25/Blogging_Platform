from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from django.contrib.auth import get_user_model
from .serializers import UserSerializer
from blog.models import BlogPost, Category, Tag
from .serializers import BlogPostSerializer, CategorySerializer, TagSerializer

User = get_user_model()

class UserViewSet(ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class BlogPostViewSet(ModelViewSet):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
