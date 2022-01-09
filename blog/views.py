from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post, Category

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
#    template_name = 'blog/single_page.html'


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