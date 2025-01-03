from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import BlogPostViewSet, UserViewSet, CategoryViewSet, TagViewSet, CommentViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Create a router for automatic URL routing based on viewsets
router = DefaultRouter()

# Register viewsets with the router
router.register(r'users', UserViewSet)
router.register(r'posts', BlogPostViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'tags', TagViewSet)
router.register(r'comments', CommentViewSet)

# Define URL patterns
urlpatterns = [
    # JWT authentication URLs
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    
    
    # Custom actions for filtering posts by category or author
    path('posts/category/<str:category_name>/', BlogPostViewSet.as_view({'get': 'posts_by_category'}), name='posts-by-category'),
    path('posts/author/<str:author_username>/', BlogPostViewSet.as_view({'get': 'posts_by_author'}), name='posts-by-author'),
]

# Include the router's URL patterns
urlpatterns += router.urls
