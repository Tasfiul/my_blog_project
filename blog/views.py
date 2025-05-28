from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import PostForm, CommentForm, CommentUpdateForm
from django.views import generic
from django.db.models import Q , BooleanField , ExpressionWrapper, F, Value # Import Q object for complex queries
from taggit.models import Tag # <--- ADD THIS IMPORT for Tag model
from django.contrib import messages
from allauth.account.decorators import verified_email_required # New import for allauth
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


 # View for creating a new blog post
@method_decorator(verified_email_required, name='dispatch')  # Ensure email is verified before accessing this view
class PostCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('blog:post_list')

    def form_valid(self, form):
        # Set the author to the current user before saving
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        # Only allow users with the 'blog.add_post' permission to create a post
        return self.request.user.is_authenticated

# View for updating an existing blog post
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def get_success_url(self):
        # Redirect to the post detail page after successful update
        return reverse_lazy('blog:post_detail', kwargs={'pk': self.object.pk})
    
    # Only allow the author to update the post
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

# View for deleting a blog post
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('blog:post_list')

    # Only allow the author to delete the post
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

# View for updating a comment
class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentUpdateForm
    template_name = 'blog/comment_update.html'

    def get_success_url(self):
        # Redirect to the post detail page after successful update
        return reverse_lazy('blog:post_detail', kwargs={'pk': self.object.post.pk})

    # Only allow the author to update the comment
    def test_func(self):
        comment = self.get_object()
        return self.request.user.username == comment.author

# View for deleting a comment
class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'
    success_url = reverse_lazy('blog:post_detail')

    def get_success_url(self):
        # Redirect to the post detail page after successful deletion
        return reverse_lazy('blog:post_detail', kwargs={'pk': self.object.post.pk})
    
    # Only allow the author to delete the comment
    def test_func(self):
        comment = self.get_object()
        return self.request.user.username == comment.author

# View for creating a new comment
@method_decorator(verified_email_required, name='dispatch')  # Ensure email is verified before accessing this view
class CommentCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Comment
    fields = ['content']
    template_name = 'blog/comment_form.html'

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
    
    def test_func(self):
        # Only allow the user to create a comment if they are logged in
        return self.request.user.is_authenticated

# View for listing all blog posts
class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    ordering = ['-pub_date']  # Order by creation date, newest first
    # Filter posts based on search query
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Ensure posts is a paginated object
        queryset = self.get_queryset()
        paginator = Paginator(queryset, 10)  # 10 posts per page
        page = self.request.GET.get('page')
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
        context['posts'] = posts
        return context
    
    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')

        queryset = queryset.annotate(
            is_staff_or_admin=ExpressionWrapper(
                Q(author__is_staff=True) | Q(author__is_superuser=True),
                output_field=BooleanField()
            )
        )

        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | Q(content__icontains=query) | Q(tags__name__icontains=query) | Q(author__username__icontains=query)
            ).distinct()  # Use distinct to avoid duplicates if a post has multiple tags
        return queryset.order_by('-is_staff_or_admin', '-pub_date')

# View for displaying a single blog post and its comments
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

# New Class-Based View for listing posts by tag
class TaggedPostListView(PostListView): # Inherit from PostListView
    def get_queryset(self):
        # Get the tag slug from the URL (defined in urls.py as <slug:tag_slug>)
        tag_slug = self.kwargs.get('tag_slug')

        if tag_slug:
            # Filter posts that have this tag.
            # `filter(tags__slug=tag_slug)` is how taggit filters by slug.
            queryset = Post.objects.filter(tags__slug=tag_slug).order_by('pub_date')
        else:
            # Fallback to the default PostListView queryset if no tag slug is provided
            queryset = super().get_queryset()

        # IMPORTANT: Re-apply the search filter if a query exists,
        # as this view can also handle search on filtered tags
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | Q(content__icontains=query) # Use 'content' or 'text'
            ).distinct()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_slug = self.kwargs.get('tag_slug')
        if tag_slug:
            # Add the current tag object to the context.
            # This allows you to display the tag name (e.g., "Posts tagged with 'Python'")
            context['current_tag'] = get_object_or_404(Tag, slug=tag_slug)
            context['title'] = f"Posts tagged with '{context['current_tag'].name}'"
        else:
            context['title'] = "All Blog Posts" # Default title if no tag is active
        return context
    

# New: User Dashboard View
class UserDashboardView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'blog/user_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['user_posts'] = Post.objects.filter(author=user).order_by('pub_date')
        context['user_comments'] = Comment.objects.filter(author=user).order_by('created_date')
        return context