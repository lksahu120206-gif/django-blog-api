from rest_framework import generics, status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from posts.models import Post, Comment
from posts.api.serializers import (
    PostSerializer, CommentSerializer, VoteSerializer, SignupSerializer, ChangePasswordSerializer
)
from posts.api.permissions import IsAuthorOrReadOnly
from posts.services.post_service import PostService, VoteService, CommentService
from posts.selectors.post_selectors import (
    list_posts_select_related, get_post_detail, list_comments_for_post
)


class IsAuthorOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
    """
    Custom permission for post/comment author.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        # POST, PUT, PATCH, DELETE - only author
        return obj.author == request.user


class PostListCreateAPIView(generics.ListCreateAPIView):
    """
    List posts (optimized) + create new post.
    """
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        limit = self.request.query_params.get('limit')
        return PostService.get_post_list(limit=int(limit) if limit else None)

    def perform_create(self, serializer):
        PostService.create_post(
            author=self.request.user,
            title=serializer.validated_data['title'],
            content=serializer.validated_data['content']
        )


class PostDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Single post detail, update, delete (author only).
    """
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    lookup_url_kwarg = 'pk'

    def get_object(self):
        return PostService.get_post_by_id(self.kwargs['pk'])

    def perform_update(self, serializer):
        PostService.update_post(
            post=self.get_object(),
            author=self.request.user,
            title=serializer.validated_data.get('title'),
            content=serializer.validated_data.get('content')
        )


class CommentListCreateAPIView(generics.ListCreateAPIView):
    """
    Post comments list + create.
    """
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return list_comments_for_post(self.kwargs['post_id'])

    def perform_create(self, serializer):
        CommentService.create_comment(
            post_id=self.kwargs['post_id'],
            author=self.request.user,
            content=serializer.validated_data['content']
        )


class CommentDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Single comment update/delete (author only).
    """
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    queryset = Comment.objects.all()
    lookup_url_kwarg = 'comment_pk'


class VoteToggleAPIView(APIView):
    """
    Toggle vote (like/dislike) for post.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def post(self, request, post_id):
        vote_type = request.data.get('vote')
        VoteService.toggle_vote(
            post_id=post_id,
            user=request.user,
            vote_type=int(vote_type)
        )
        return Response({'message': 'Vote updated successfully'}, status=status.HTTP_200_OK)


class SignupAPIView(APIView):
    """
    User signup endpoint.
    """
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'User created successfully. Please login to get JWT tokens.',
                'username': serializer.validated_data['username']
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordAPIView(APIView):
    """
    Change password for authenticated user.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({
                'message': 'Password changed successfully.'
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

