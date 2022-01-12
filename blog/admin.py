from django.contrib import admin
from .models import Post, Category, Tag, Comment

admin.site.register(Post)
admin.site.register(Comment)

#잔고에서 제공 slug 자동화
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)

