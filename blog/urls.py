from django.urls import path
from . import views
from .feeds import LatestPostsFeed  # Import the feed class

app_name = 'blog' 

urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path('posts/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('posts/new/', views.PostCreateView.as_view(), name='post_create'),
    path('posts/<int:pk>/edit/', views.PostUpdateView.as_view(), name='post_edit'),
    path('posts/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
    path('comments/<int:pk>/update/', views.CommentUpdateView.as_view(), name='comment_update'),
    path('comments/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='comment_delete'),
    path('comments/new/<int:post_pk>/', views.CommentCreateView.as_view(), name='comment_create'),
    path('tags/<slug:tag_slug>/', views.TaggedPostListView.as_view(), name='posts_by_tag'), # <--- ADD THIS LINE
    path('dashboard/', views.UserDashboardView.as_view(), name='user_dashboard'),
        # Add this new URL pattern for the RSS Feed
    path('feed/', LatestPostsFeed(), name='latest_posts_feed'), # <--- ADD THIS LINE
]
