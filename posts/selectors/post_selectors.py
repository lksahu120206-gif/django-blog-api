from django.db.models import Prefetch, Count, Q
from posts.models import Post, Comment, Vote


def list_posts_select_related(prefetch_comments=True, limit=None):
    """
    Optimized post list query with select_related and prefetch_related.
    Returns posts ordered by created_at with aggregated vote counts.
    """
    queryset = Post.objects.select_related('author').annotate(
        likes_count=Count('votes', filter=Q(votes__vote=1)),
        dislikes_count=Count('votes', filter=Q(votes__vote=-1)),
        comments_count=Count('comments')
    ).order_by('-created_at')
    
    if prefetch_comments:
        queryset = queryset.prefetch_related(
            Prefetch('comments', queryset=Comment.objects.select_related('author')[:3])
        )
    
    if limit:
        queryset = queryset[:limit]
    
    return queryset


def get_post_detail(post_id):
    """
    Optimized post detail query.
    """
    return Post.objects.select_related('author').prefetch_related(
        Prefetch(
            'comments',
            queryset=Comment.objects.select_related('author').order_by('-created_at'),
            to_attr='comment_list'
        ),
        Prefetch(
            'votes',
            queryset=Vote.objects.none(),
            to_attr='all_votes'
        )
    ).annotate(
        likes_count=Count('votes', filter=Q(votes__vote=1)),
        dislikes_count=Count('votes', filter=Q(votes__vote=-1))
    ).get(pk=post_id)


def list_comments_for_post(post_id):
    """
    Optimized comment list for post.
    """
    return Comment.objects.filter(post_id=post_id).select_related('author', 'post').order_by('-created_at')


def get_user_votes(post_id, user):
    """
    Get user vote for specific post.
    """
    return Vote.objects.filter(post_id=post_id, user=user).first()

