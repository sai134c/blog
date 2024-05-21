from django.contrib import admin
from .models import Post, PostAttachment
from .forms import PostForm

class PostAdmin(admin.ModelAdmin):
    list_display = ('id','author','time_stamp','text')
    list_filter = ('time_stamp',)
    search_fields = ('text','time_stamp')
    ordering = ('id',)
    form = PostForm
    

admin.site.register(Post,PostAdmin)
admin.site.register(PostAttachment)