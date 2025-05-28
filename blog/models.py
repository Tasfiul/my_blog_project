from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from tinymce.models import HTMLField
from taggit.managers import TaggableManager

class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    content = HTMLField()
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    tags = TaggableManager(blank=True, help_text="Add tags to your post. Separate with commas.")

    def publish(self):
        self.pub_date = timezone.now()
        self.save()

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.pk})
    def get_update_url(self):
        return reverse('blog:post_update', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-pub_date']
        permissions = [
            ("can_publish", "Can publish posts"),
            ("can_unpublish", "Can unpublish posts"),
        ]

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=100)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    

    class Meta:
        ordering = ['created_date']
        permissions = [
            ("can_create_comment", "Can create comment"),
            ("can_edit_comment", "Can edit comment"),
            ("can_delete_comment", "Can delete comment"),
        ]

    def __str__(self):
        return f'Comment by {self.author} on {self.post}'
