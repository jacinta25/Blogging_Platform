from rest_framework.generics import ListCreateAPIView
from .models import BlogPost
from .serializers import BlogPostSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication

class BlogPostListCreateView(ListCreateAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer




class SecuredPostListView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Just a dummy response to demonstrate
        data = {"message": "This is a secured API endpoint."}
        return Response(data)

