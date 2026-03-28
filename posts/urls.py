from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
from .views import (
    PostListCreateView,
    PostDetailView,
    CommentListCreateView,
    CommentDetailView,
    VoteToggleView,
    SignupAPIView
)

urlpatterns = [
    # AUTH - SimpleJWT
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('signup/', SignupAPIView.as_view(), name='signup'),

    # POSTS
    path('posts/', PostListCreateView.as_view(), name='post-list'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),

    # COMMENTS
    path('posts/<int:post_id>/comments/', CommentListCreateView.as_view(), name='post-comments'),
    path('comments/<int:pk>/', CommentDetailView.as_view(), name='comment-detail'),

    # VOTES
    path('posts/<int:post_id>/vote/', VoteToggleView.as_view(), name='post-vote'),
]
