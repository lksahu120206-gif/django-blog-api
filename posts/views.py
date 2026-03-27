from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from .models import Post, Comment, Vote
from .serializers import PostSerializer, CommentSerializer, VoteSerializer


# Post Permission
class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


# Comment Permission
class IsCommentAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


# Post List + Create
class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


# Post Detail
class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]


# Comment List + Create
class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        return Comment.objects.filter(post_id=post_id)

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            post_id=self.kwargs['post_id']
        )


# Comment Detail (edit/delete)
class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsCommentAuthorOrReadOnly]

# Vote Toggle (like/dislike)
class VoteToggleView(generics.CreateAPIView):
    serializer_class = VoteSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request, *args, **kwargs):
        post_id = kwargs['post_id']
        vote_type = int(request.data.get('vote'))
        if vote_type not in [1, -1]:
            return Response({'error': 'Vote must be 1 (like) or -1 (dislike)'}, status=400)

        vote, created = Vote.objects.get_or_create(
            post_id=post_id,
            user=request.user,
            defaults={'vote': vote_type}
        )
        if not created:
            vote.vote = vote_type
            vote.save()

        return Response({'message': 'Vote updated', 'vote': vote_type})

def home(request):
    return render(request, "blog_app/index.html")
