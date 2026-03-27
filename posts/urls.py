from django.urls import path
from .views import (
    PostListCreateView,
    PostDetailView,
    CommentListCreateView,
    CommentDetailView,
    VoteToggleView
)

urlpatterns = [
    # Auth
    path('signup/', SignupAPIView.as_view()),
    
    # Posts
    path('posts/', PostListCreateView.as_view()),
    path('posts/<int:pk>/', PostDetailView.as_view()),

    # Comments
    path('posts/<int:post_id>/comments/', CommentListCreateView.as_view()),
    path('comments/<int:pk>/', CommentDetailView.as_view()),
    # Vote
    path('posts/<int:post_id>/vote/', VoteToggleView.as_view()),
]
