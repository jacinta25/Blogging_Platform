from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin
from blog.models import BlogPost

@admin.register(BlogPost)
class BlogPostAdmin(MarkdownxModelAdmin):
    list_display = ['title', 'author', 'published_date']
