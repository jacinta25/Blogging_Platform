from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import (
    BlogPostViewSet,
    UserViewSet,
    CategoryViewSet,
    TagViewSet,
    CommentViewSet,
    UserLoginView,
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Create a router for automatic URL routing based on viewsets
router = DefaultRouter()

# Register viewsets with the router
router.register('users', UserViewSet)
router.register('posts', BlogPostViewSet)
router.register('categories', CategoryViewSet)
router.register('tags', TagViewSet)
router.register('comments', CommentViewSet)

# Define URL patterns
urlpatterns = [
    # JWT authentication endpoints
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

     # Your custom login view, if needed
    path('api/users/login/', UserLoginView.as_view(), name='user_login'),
    # Custom actions for BlogPostViewSet
    path('posts/category/<str:category_name>/', 
         BlogPostViewSet.as_view({'get': 'posts_by_category'}), 
         name='posts-by-category'),
    path('posts/author/<str:author_username>/', 
         BlogPostViewSet.as_view({'get': 'posts_by_author'}), 
         name='posts-by-author'),

    # Custom actions for Post Likes and Ratings
    path('posts/<int:pk>/like/', 
         BlogPostViewSet.as_view({'post': 'like_post'}), 
         name='like-post'),
    path('posts/<int:pk>/rate/', 
         BlogPostViewSet.as_view({'post': 'rate_post'}), 
         name='rate-post'),
    path('posts/most-liked/', 
         BlogPostViewSet.as_view({'get': 'most_liked'}), 
         name='most-liked-posts'),
    path('posts/highest-rated/', 
         BlogPostViewSet.as_view({'get': 'highest_rated'}), 
         name='highest-rated-posts'),

    # Custom action to share a post via email
    path('posts/<int:pk>/share/', 
         BlogPostViewSet.as_view({'post': 'share_post'}), 
         name='share-post'),

    # Custom actions for UserViewSet
    path('users/<int:pk>/subscribe/', 
         UserViewSet.as_view({'post': 'subscribe_to_author'}), 
         name='subscribe-to-author'),
    path('users/<int:pk>/unsubscribe/', 
         UserViewSet.as_view({'delete': 'unsubscribe_from_author'}), 
         name='unsubscribe-from-author'),
]

# Include the router's URL patterns
urlpatterns += router.urls
