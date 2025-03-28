from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter
from .views import PostViewSet, CommentViewSet, FeedView


# Main Router (For Posts)
router = DefaultRouter()
router.register('posts', PostViewSet, basename='post')

# Nested Router (For Comments inside Posts)
post_router = NestedDefaultRouter(router, 'posts', lookup='post')  # 'post' will be used in URLs
post_router.register('comments', CommentViewSet, basename='post-comments')

# The API URLs are now automatically determined by the router
urlpatterns = [
    path('', include(router.urls)),
    path('', include(post_router.urls)),
    path('feed/', FeedView.as_view(), name='user-feed'),
]
