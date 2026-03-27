from django.core.exceptions import ValidationError
from django.db import transaction
from posts.selectors.post_selectors import (
    list_posts_select_related, 
    get_post_detail, 
    list_comments_for_post,
    get_user_votes
)
from posts.models import Post, Vote, Comment


class PostService:
    @staticmethod
    @transaction.atomic
    def create_post(author, title, content):
        """
        Create post with validation.
        """
        if not title or not content:
            raise ValidationError('Title and content are required')
        
        return Post.objects.create(
            author=author,
            title=title,
            content=content
        )

    @staticmethod
    def get_post_list(limit=None):
        """
        Get optimized post list.
        """
        return list_posts_select_related(limit=limit)

    @staticmethod
    def get_post_by_id(post_id):
        """
        Get single post with optimized queries.
        """
        try:
            return get_post_detail(post_id)
        except Post.DoesNotExist:
            raise ValidationError('Post not found')

    @staticmethod
    def update_post(post, author, title, content):
        """
        Update post (author check in permission).
        """
        if title is not None:
            post.title = title
        if content is not None:
            post.content = content
        post.save()
        return post


class VoteService:
    @staticmethod
    @transaction.atomic
    def toggle_vote(post_id, user, vote_type):
        """
        Toggle user vote (1=like, -1=dislike).
        Toggle if exists, create if not.
        """
        if vote_type not in [1, -1]:
            raise ValidationError('Vote must be 1 (like) or -1 (dislike)')

        vote, created = Vote.objects.get_or_create(
            post_id=post_id,
            user=user,
            defaults={'vote': vote_type}
        )

        if not created:
            vote.vote = vote_type
            vote.save()
        
        return vote


class CommentService:
    @staticmethod
    @transaction.atomic
    def create_comment(post_id, author, content):
        """
        Create comment for post.
        """
        if not content.strip():
            raise ValidationError('Comment cannot be empty')

        return Comment.objects.create(
            post_id=post_id,
            author=author,
            content=content.strip()
        )

