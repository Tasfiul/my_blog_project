from django.shortcuts import render
from .models import Post, Comment
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import PostForm

class PostCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('blog:post_list')
    permission_required = 'blog.add_post'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, PermissionRequiredMixin,UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    permission_required = 'blog.change_post'
    permission_denied_message = 'You do not have permission to edit this post.'
    def get_success_url(self):
        # Redirect to the post detail page after successful update
        return reverse_lazy('blog:post_detail', kwargs={'pk': self.object.pk})
    
    # Define the test for UserPassesTestMixin (object-level permission)
    def test_func(self):
        # Get the post object being viewed/edited
        post = self.get_object()
        # Return True if the logged-in user is the author of the post
        return self.request.user == post.author

class PostDeleteView(LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('blog:post_list')
    permission_required = 'blog.delete_post'

    def test_func(self):
        # Get the post object being viewed for deletion
        post = self.get_object()
        # Return True if the logged-in user is the author of the post
        return self.request.user == post.author

class CommentUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    fields = ['content']
    template_name = 'blog/comment_form.html'
    permission_required = 'blog.change_comment'
    permission_denied_message = 'You do not have permission to edit this comment.'

    def get_success_url(self):
        # Redirect to the post detail page after successful update
        return reverse_lazy('blog:post_detail', kwargs={'pk': self.object.post.pk})

    def test_func(self):
        # Get the comment object being viewed/edited
        comment = self.get_object()
        # Return True if the logged-in user is the author of the comment
        return self.request.user == comment.author

class CommentDeleteView(LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'
    success_url = reverse_lazy('blog:post_list')
    permission_required = 'blog.delete_comment'

    def get_success_url(self):
        # Redirect to the post detail page after successful deletion
        return reverse_lazy('blog:post_detail', kwargs={'pk': self.object.post.pk})
    
    def test_func(self):
        # Get the comment object being viewed for deletion
        comment = self.get_object()
        # Return True if the logged-in user is the author of the comment
        return self.request.user == comment.author

class CommentCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Comment
    fields = ['content']
    template_name = 'blog/comment_form.html'
    permission_required = 'blog.add_comment'

    def get_success_url(self):
        # Redirect to the post detail page after successful creation
        return reverse_lazy('blog:post_detail', kwargs={'pk': self.kwargs['post_pk']})
    def form_valid(self, form):
        # Set the post for the comment
        form.instance.post_id = self.kwargs['post_pk']
        # Set the author of the comment
        form.instance.author = self.request.user
        return super().form_valid(form)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = Post.objects.get(pk=self.kwargs['post_pk'])
        return context

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 10

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

