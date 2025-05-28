from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from blog.sitemaps import PostSitemap

urlpatterns = [
    path('tinymce/', include('tinymce.urls')),
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
    #path('accounts/', include('django.contrib.auth.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': {'posts': PostSitemap}}, name='django.contrib.sitemaps.views.sitemap'),
    #path('register/', include('users.urls')),
    path('accounts/', include('allauth.urls')), # Add this line for allauth URLs
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)