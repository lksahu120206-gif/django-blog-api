from django.urls import path
from django.http import JsonResponse

from .views import (
    PostListCreateView,
    PostDetailView,
    CommentListCreateView,
    CommentDetailView,
    VoteToggleView,
    signup,
    SignupAPIView
)

def test(request):
    return JsonResponse({"status": "API WORKING", "signup_available": True})

urlpatterns = [
    # Test
    path('test/', test, name='test'),

    # Auth
    path('signup/', signup, name='signup'),
    path('auth/signup/', SignupAPIView.as_view(), name='auth-signup'),

    # Posts
    path('posts/', PostListCreateView.as_view(), name='post-list'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),

    # Comments
    path('posts/<int:post_id>/comments/', CommentListCreateView.as_view(), name='post-comments'),
    path('comments/<int:pk>/', CommentDetailView.as_view(), name='comment-detail'),

    # Votes
    path('posts/<int:post_id>/vote/', VoteToggleView.as_view(), name='post-vote'),
]