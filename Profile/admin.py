from django.contrib import admin
from django.utils.safestring import mark_safe
from Profile.models import PostWall, Reviews, LikePost

class PostWallAdmin(admin.ModelAdmin):
    list_display = ('id', 'des', 'user', 'get_image')
    def get_image(self, obj):
        if obj.image:
            return mark_safe(f'<img src={obj.image.url} width="50" height="60" style="margin-left: 0px;" ')
        else:
            return None


    get_image.short_description = "Изображение"
    get_image.allow_tags = True

admin.site.register(PostWall, PostWallAdmin)
admin.site.register(Reviews)
admin.site.register(LikePost)
