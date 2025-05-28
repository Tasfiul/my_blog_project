from django import forms
from .models import Post, Comment
from tinymce.widgets import TinyMCE


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image', 'tags']

# Form for creating new comments (if you have one, ensure it's here)
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        # exclude = ['author', 'post', 'date_posted'] # Alternatively, use exclude if you have many fields

# Form for updating existing comments (add this)
class CommentUpdateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content'] # Only allow editing the text content of the comment