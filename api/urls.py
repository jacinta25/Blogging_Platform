from rest_framework.routers import DefaultRouter
from .views import BlogPostViewSet, UserViewSet, CategoryViewSet, TagViewSet

#authentication
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    )
from django.urls import path 


router = DefaultRouter()


router.register('users', UserViewSet)
router.register('posts', BlogPostViewSet)
router.register('categories', CategoryViewSet)
router.register('tags', TagViewSet)


urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
]

urlpatterns += router.urls