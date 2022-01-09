from django.contrib import admin
from .models import Post, Category

admin.site.register(Post)

#잔고에서 제공 slug 자동화
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Category, CategoryAdmin)