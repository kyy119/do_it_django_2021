from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.utils.text import slugify
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import Post, Category, Tag
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


#CBV(Class Based View)로 블로스 포스트 목록 페이지 만들기
class PostList(ListView):
    model = Post
#    template_name = 'blog/index.html'
    ordering = '-pk'
    def get_context_data(self, **kwargs):
        context = super(PostList, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        return context


#CBV(Class Based View)로 블로스 상세 페이지 만들기
class PostDetail(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        return context
#    template_name = 'blog/single_page.html'


class PostCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Post
    fields = ['title', 'hook_text', 'content', 'head_image', 'file_upload', 'category']

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff
    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated and (current_user.is_staff or current_user.is_superuser):
            form.instance.author = current_user

            response = super(PostCreate, self).form_valid(form)
            tags_str = self.request.POST.get('tags_str')
            if tags_str:
                tags_str = tags_str.strip()
                tags_str = tags_str.replace(',', ';')
                tags_list = tags_str.split(';')

                for t in tags_list:
                    t = t.strip()
                    tag, is_tag_created = Tag.objects.get_or_create(name=t)
                    if is_tag_created:
                        tag.slug = slugify(t, allow_unicode=True)
                        tag.save()
                    self.object.tags.add(tag)
            return response
        else:
            return redirect('/blog/')


class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['title', 'hook_text', 'content', 'head_image', 'file_upload', 'category']

    # url이 get,post 방식인지 구분 하는 역할 해당하는 포스트의 권한이 있는 user인지 확인
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(PostUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied
        # PermissionDenied 잔고에서 제공해주는 기능 권한이 없는걸 알려주는 메세지를 준다.

    template_name = 'blog/post_update_form.html'

def category_page(request, slug):
    if slug == 'no_category':
        category = '미분류'
        post_list = Post.objects.filter(category=None)
    else:
        category = Category.objects.get(slug=slug)
        post_list = Post.objects.filter(category=category)
    return render(
        request,
        'blog/post_list.html',
        {
            'post_list': post_list,
            'categories': Category.objects.all(),
            'no_category_post_count': Post.objects.filter(category=None).count(),
            'category': category
        }
    )


def tag_page(request, slug):
    tag = Tag.objects.get(slug=slug)
    post_list = tag.post_set.all()
    return render(
        request,
        'blog/post_list.html',
        {
            'post_list': post_list,
            'categories': Category.objects.all(),
            'no_category_post_count': Post.objects.filter(category=None).count(),
            'tag': tag
        }
    )


#FBV(Function Based view) 블리스 리스트 페이지
#def index(request):
#    posts = Post.objects.all().order_by('-pk')
#    return render(
#        request,
#        'blog/index.html',
#        {
#            'posts': posts,
#        }
#    )
#FBV(Function Based view) 블로스 상세 페이지 만들기
#def single_post_page(request, pk):
#    post = Post.objects.get(pk=pk)
#    return render(
#        request,
#        'blog/single_page.html',
#        {
#            'post': post,
#        }
#    )