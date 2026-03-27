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

# ✅ TEST ROUTE
def test(request):
    return JsonResponse({"status": "API WORKING"})

urlpatterns = [
    # 🔥 TEST
    path('test/', test, name='test'),

    # 🔥 AUTH
    path('signup/', signup, name='signup'),
    path('auth/signup/', SignupAPIView.as_view(), name='auth-signup'),

    # POSTS
    path('posts/', PostListCreateView.as_view(), name='post-list'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),

    # COMMENTS
    path('posts/<int:post_id>/comments/', CommentListCreateView.as_view(), name='post-comments'),
    path('comments/<int:pk>/', CommentDetailView.as_view(), name='comment-detail'),

    # VOTES
    path('posts/<int:post_id>/vote/', VoteToggleView.as_view(), name='post-vote'),
]