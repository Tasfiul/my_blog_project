from django.shortcuts import render
from .models import Post, Comment
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import PostForm
from django.db.models import Q # Import Q object for complex queries

# View for creating a new blog post
class PostCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('blog:post_list')
    permission_required = 'blog.add_post'

    def form_valid(self, form):
        # Set the author to the current user before saving
        form.instance.author = self.request.user
        return super().form_valid(form)

# View for updating an existing blog post
class PostUpdateView(LoginRequiredMixin, PermissionRequiredMixin,UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    permission_required = 'blog.change_post'
    permission_denied_message = 'You do not have permission to edit this post.'

    def get_success_url(self):
        # Redirect to the post detail page after successful update
        return reverse_lazy('blog:post_detail', kwargs={'pk': self.object.pk})
    
    # Only allow the author to update the post
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

# View for deleting a blog post
class PostDeleteView(LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('blog:post_list')
    permission_required = 'blog.delete_post'

    # Only allow the author to delete the post
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

# View for updating a comment
class CommentUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    fields = ['content']
    template_name = 'blog/comment_form.html'
    permission_required = 'blog.change_comment'
    permission_denied_message = 'You do not have permission to edit this comment.'

    def get_success_url(self):
        # Redirect to the post detail page after successful update
        return reverse_lazy('blog:post_detail', kwargs={'pk': self.object.post.pk})

    # Only allow the author to update the comment
    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

# View for deleting a comment
class CommentDeleteView(LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'
    success_url = reverse_lazy('blog:post_list')
    permission_required = 'blog.delete_comment'

    def get_success_url(self):
        # Redirect to the post detail page after successful deletion
        return reverse_lazy('blog:post_detail', kwargs={'pk': self.object.post.pk})
    
    # Only allow the author to delete the comment
    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

# View for creating a new comment
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
        # Add the related post to the context for use in the template
        context = super().get_context_data(**kwargs)
        context['post'] = Post.objects.get(pk=self.kwargs['post_pk'])
        return context

# View for listing all blog posts
class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 10  # Show 10 posts per page
    ordering = ['pub_date']  # Order by creation date, newest first
    # Filter posts based on search query
    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | Q(content__icontains=query)
            )
        return queryset

# View for displaying a single blog post and its comments
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

