from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register('posts', PostViewSet, basename='post')
router.register('comments', CommentViewSet, basename='comment')

# The API URLs are now automatically determined by the router
urlpatterns = [
    path('', include(router.urls)),
]
