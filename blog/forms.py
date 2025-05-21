from django import forms
from .models import Post, Comment
from tinymce.widgets import TinyMCE


class PostForm(forms.ModelForm):
    content = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))
    class Meta:
        model = Post
        fields = ['title', 'content', 'image']
