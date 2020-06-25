from django.contrib import admin
from blog.models import Items, Viewers, PostLikes


# Register your models here.

class ViewAdmin(admin.TabularInline):
        model = Viewers


class PostLikesAdmin(admin.TabularInline):
        model = PostLikes


class ItemAdmin(admin.ModelAdmin):
    inlines = [ViewAdmin, PostLikesAdmin]
    list_display =['title', 'created_at', 'owner', 'author', 'owner_info']

    search_feild = ['title']

    class Meta:
        model = Items


admin.site.register(Items, ItemAdmin)