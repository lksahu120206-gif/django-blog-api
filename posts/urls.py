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
    return JsonResponse({
        "status": "API WORKING",
        "signup_available": True
    })

urlpatterns = [
    path('test/', test),

    path('signup/', signup),
    path('auth/signup/', SignupAPIView.as_view()),

    path('posts/', PostListCreateView.as_view()),
    path('posts/<int:pk>/', PostDetailView.as_view()),

    path('posts/<int:post_id>/comments/', CommentListCreateView.as_view()),
    path('comments/<int:pk>/', CommentDetailView.as_view()),

    path('posts/<int:post_id>/vote/', VoteToggleView.as_view()),
]
