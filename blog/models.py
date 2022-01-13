from django.db import models
from django.contrib.auth.models import User
import os
from markdownx.utils import markdown

from markdownx.models import MarkdownxField
from datetime import timedelta

class Category(models.Model):
    #unique -> 카테고르 중복 x
    name = models.CharField(max_length=50, unique=True)
    #allow_unicode -> 한글도 쓸 수 있게 해준다.
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/blog/category/{self.slug}/'

    #categorys->categories 복수형 바꾸기
    class Meta:
        verbose_name_plural = 'Categories'

class Tag(models.Model):
    #unique -> 카테고르 중복 x
    name = models.CharField(max_length=50, unique=True)
    #allow_unicode -> 한글도 쓸 수 있게 해준다.
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/blog/tag/{self.slug}/'

class Post(models.Model):
    title = models.CharField(max_length=50)
    hook_text = models.CharField(max_length=100, blank=True)
    content = MarkdownxField()

    head_image = models.ImageField(upload_to='blog/images/%y/%m/%d/', blank=True)
    file_upload = models.FileField(upload_to='blog/files/%y/%m/%d/', blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    #작성자 삭제시 게시물도 같이 삭제
    #author = models.ForeignKey(User, on_delete=models.CASCADE)
    #작성자 삭제시 게시물 삭제 x
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    #form에 필수 사항에 다 들어갔는지 확인 하는 것이 blank=True
    #Null=True 는 데이터베이스안에 정보가 있어야된다 없어야 된다 정의 하는것
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
    #다대다 관계
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return f'[{self.pk}] {self.title} :: {self.author}'

    def get_absolute_url(self):
        return f'/blog/{self.pk}/'

    def get_file_name(self):
        return os.path.basename(self.file_upload.name)

    def get_file_ext(self):
        return self.get_file_name().split('.')[-1]

    def get_content_markdown(self):
        return markdown(self.content)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.author}::{self.content}'

    def get_absolute_url(self):
        return f'{self.post.get_absolute_url()}#comment-{self.pk}'

    def is_updated(self):
        return self.updated_at - self.created_at > timedelta(seconds=1)

    def get_avatar_url(self):
        if self.author.socialaccount_set.exists():
            return self.author.socialaccount_set.first().get_avatar_url()
        else:
            return f'https://doitdjango.com/avatar/id/143/e3445497d896a175/svg/{self.author.email}'
