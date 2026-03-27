from django.urls import path
from .api.views import (
    PostListCreateAPIView, 
    PostDetailAPIView, 
    CommentListCreateAPIView, 
    CommentDetailAPIView, 
    VoteToggleAPIView,
    SignupAPIView,
    ChangePasswordAPIView
)
from django.http import HttpResponse

def test(request):
    return HttpResponse("API WORKING")

from .views import signup

urlpatterns = [
    # Auth
    path('signup/', signup, name='signup'),
    path('auth/signup/', SignupAPIView.as_view(), name='auth-signup'),
    path('auth/change-password/', ChangePasswordAPIView.as_view(), name='change-password'),
    
    # Posts
    path('posts/', PostListCreateAPIView.as_view(), name='post-list'),
    path('posts/<int:pk>/', PostDetailAPIView.as_view(), name='post-detail'),
    
    # Comments
    path('posts/<int:post_id>/comments/', CommentListCreateAPIView.as_view(), name='post-comments'),
    path('comments/<int:pk>/', CommentDetailAPIView.as_view(), name='comment-detail'),
    
    # Votes
    path('posts/<int:post_id>/vote/', VoteToggleAPIView.as_view(), name='post-vote'),
    path('test/', test, name='test'),
]

