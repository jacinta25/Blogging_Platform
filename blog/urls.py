from django.urls import path
from .views import BlogPostListCreateView

urlpatterns = [
    path('posts/', BlogPostListCreateView.as_view(), name='blogpost-list-create'),
]
