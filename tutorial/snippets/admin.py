from django.contrib import admin
from snippets.models import Snippet

# Register your models here.

class SnippetAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        # "url",
        "owner",
        "title",
        "code",
        "linenos",
        "language",
        "style",
        # "highlight",
    ]


admin.site.register(Snippet, SnippetAdmin)