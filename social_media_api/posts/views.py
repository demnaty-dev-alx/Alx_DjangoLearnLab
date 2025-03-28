from rest_framework import viewsets, permissions, filters
from rest_framework.exceptions import PermissionDenied
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer

class PostViewSet(viewsets.ModelViewSet):
    """
    API endpoint for creating, retrieving, updating, and deleting posts.
    """
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]  # Only authenticated users can interact
    queryset = Post.objects.all().order_by('-created_at')

    filter_backends = [filters.SearchFilter]  # Enables search filtering
    search_fields = ['title', 'content']  # Searchable fields

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)  # Set the logged-in user as the author

    def perform_update(self, serializer):
        if self.get_object().author != self.request.user:
            raise PermissionDenied("You do not have permission to edit this post.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied("You do not have permission to delete this post.")
        instance.delete()


class CommentViewSet(viewsets.ModelViewSet):
    """
    API endpoint for creating, retrieving, updating, and deleting comments.
    """
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Comment.objects.all().order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        if self.get_object().author != self.request.user:
            raise PermissionDenied("You do not have permission to edit this comment.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied("You do not have permission to delete this comment.")
        instance.delete()
