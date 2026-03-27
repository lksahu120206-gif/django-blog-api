from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from taggit.models import Tag
from .models import Post, Comment
from .forms import EmailPostForm, CommentForm

class PostListView(ListView):
    model = Post
    template_name = 'blog/post/list.html'
    context_object_name = 'posts'
    queryset = Post.objects.filter(status='published')
    paginate_by = 3

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post/detail.html'
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = self.object
            comment.save()
            context = self.get_context_data(object=self.object)
            context['new_comment'] = comment
            return self.render_to_response(context)
        else:
            context = self.get_context_data(object=self.object, comment_form=comment_form)
            return self.render_to_response(context)

    def get_object(self, queryset=None):
        post = get_object_or_404(Post, 
            slug=self.kwargs['post'],
            status='published',
            publish__year=self.kwargs['year'],
            publish__month=self.kwargs['month'],
            publish__day=self.kwargs['day']
        )
        return post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.filter(active=True)
        context['comment_form'] = CommentForm()
        return context

def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read {post.title}"
            message = f"""
{cd['name']} recommends you read "{post.title}"

Link:
{post_url}

Comments:
{cd['comments']}
"""
            send_mail(subject, message, from_email=None, recipient_list=[cd['email_to']])
            sent = True
        else:
            form = EmailPostForm()
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and sent:
        return JsonResponse({'success': True, 'email_to': cd['email_to']})
    return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent})

def post_list_by_tag(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    posts = Post.objects.filter(tags__in=[tag], status='published')
    paginator = Paginator(posts, 3)
    page = request.GET.get('page')
    try:
        posts_page = paginator.page(page)
    except PageNotAnInteger:
        posts_page = paginator.page(1)
    except EmptyPage:
        posts_page = paginator.page(paginator.num_pages)
    return render(
        request,
        'blog/post/list.html',
        {
            'page_obj': posts_page,
            'tag': tag,
        }
    )
