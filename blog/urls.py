from django.urls import path
from .views import BlogPostListCreateView
from .views import SecuredPostListView


urlpatterns = [
    path('posts/', BlogPostListCreateView.as_view(), name='blogpost-list-create'),
    path('api/secured-posts/', SecuredPostListView.as_view(), name='secured-posts'),

]
