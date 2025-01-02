from rest_framework.routers import DefaultRouter
from .views import BlogPostViewSet, UserViewSet, CategoryViewSet, TagViewSet


router = DefaultRouter()


router.register('users', UserViewSet)
router.register('blogs', BlogPostViewSet)
router.register('categories', CategoryViewSet)
router.register('tags', TagViewSet)


urlpatterns = [] + router.urls