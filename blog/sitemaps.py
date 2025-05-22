from django.contrib.sitemaps import Sitemap
from .models import Post
from django.urls import reverse


class PostSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return Post.objects.all()

    def lastmod(self, obj):
        return obj.pub_date  # or obj.modified, depending on your model

    def location(self, obj):
        # The full path to the object's page
        return reverse('blog:post_detail', args=[obj.pk])