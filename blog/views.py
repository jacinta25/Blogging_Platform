from rest_framework.generics import ListCreateAPIView
from .models import BlogPost
from .serializers import BlogPostSerializer

class BlogPostListCreateView(ListCreateAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer

