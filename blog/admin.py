from django.contrib import admin
from .models import Post, Comment

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    fields = ['author', 'post', 'created_date']
    readonly_fields = ['created_date']

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'pub_date')
    search_fields = ('title', 'content')
    list_filter = ('pub_date','author')
    ordering = ('pub_date',)
    inlines = [CommentInline]

    fieldsets = (
        (None, {
            'fields': ('title', 'author')
        }),
        ('Content', {
            'fields': ('content',)
        }),
    )
    def save_model(self, request, obj, form, change):
        if not change or not obj.author:
            obj.author = request.user
        super().save_model(request, obj, form, change)

admin.site.register(Post, PostAdmin)
admin.site.register(Comment)

# Register your models here.
