from rest_framework import viewsets, generics,permissions, filters, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType
from posts.models import Post, Comment, Like
from posts.serializers import PostSerializer, CommentSerializer, LikeSerializer
from notifications.models import Notification



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

class FeedView(generics.ListAPIView):
    """
    Returns a feed of posts from users the authenticated user follows.
    """
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        following_users = user.following.all()  # Get all users the authenticated user follows
        return Post.objects.filter(author__in=following_users).order_by('-created_at')


class LikePostView(APIView):
    """
    Allows a user to like a post.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)

        # Check if the user has already liked this post
        if Like.objects.filter(user=request.user, post=post).exists():
            return Response({"error": "You have already liked this post."}, status=status.HTTP_400_BAD_REQUEST)

        # Create a like instance
        like = Like.objects.create(user=request.user, post=post)

        # Create a notification for the post author
        if post.author != request.user:  # Avoid self-notification
            Notification.objects.create(
                recipient=post.author,
                actor=request.user,
                verb="liked your post",
                target=post,
                target_ct=ContentType.objects.get_for_model(post)
            )

        serializer = LikeSerializer(like)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UnlikePostView(APIView):
    """
    Allows a user to unlike a post.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)

        # Check if the user has liked the post
        like = Like.objects.filter(user=request.user, post=post).first()
        if not like:
            return Response({"error": "You have not liked this post."}, status=status.HTTP_400_BAD_REQUEST)

        # Remove the like
        like.delete()

        return Response({"message": "Post unliked successfully."}, status=status.HTTP_200_OK)
