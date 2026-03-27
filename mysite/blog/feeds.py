from django.contrib.syndication.views import Feed
from django.urls import reverse_lazy
from .models import Post

class LatestPostsFeed(Feed):
    title = "My Blog"
    link = reverse_lazy('blog:post_list')
    description = "New posts from my blog"

    def items(self):
        return Post.published.order_by('-publish')[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.body

    def item_pubdate(self, item):
        return item.publish
