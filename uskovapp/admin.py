from django.contrib import admin
from uskovapp import models

# Register your models here.


class CommentVersionInline(admin.TabularInline):
    model = models.CommentVersions
    

class CommentsAdmin(admin.ModelAdmin):
    inlines = [CommentVersionInline]

    
class VariantInline(admin.TabularInline):
    model = models.PollVariants

    
class PollAdmin(admin.ModelAdmin):
    inlines = [VariantInline]
    

admin.site.register(models.Comments, CommentsAdmin)
admin.site.register(models.Polls, PollAdmin)