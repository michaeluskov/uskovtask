from django.contrib import admin
from uskovapp import models

# Register your models here.


class CommentVersionInline(admin.TabularInline):
    model = models.CommentVersions
    

class CommentsAdmin(admin.ModelAdmin):
    inlines = [CommentVersionInline]
    

admin.site.register(models.Comments, CommentsAdmin)