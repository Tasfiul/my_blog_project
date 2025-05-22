# my_blog_project/blog/feeds.py

from django.contrib.syndication.views import Feed
from django.urls import reverse
from django.utils.html import strip_tags
from .models import Post # Import your Post model

class LatestPostsFeed(Feed):
    title = "My Awesome Blog Latest Posts"
    link = "/" # The main link for your blog
    description = "Updates on the latest blog posts from My Awesome Blog."

    def items(self):
        # Return the 5 most recently published posts
        return Post.objects.filter(pub_date__isnull=False).order_by('pub_date')[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        # Use item.content or item.text, depending on your Post model field
        # You might want to truncate this for RSS feeds, or use a rich text field
        # For simplicity, we'll use a plain text summary here.
        # If TinyMCE's content can be HTML, you might want to use item.content or clean it.
        # For now, let's just return the full content (which will be HTML if using TinyMCE)
        summary = strip_tags(item.content)  # Remove HTML tags from TinyMCE content
        summary = summary.strip()
        return summary[:200] + ('...' if len(summary) > 200 else '')

    def item_link(self, item):
        return reverse('blog:post_detail', args=[item.pk])