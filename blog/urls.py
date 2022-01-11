from django.urls import path
from . import views

#FBV(Function Based view)일때
#urlpatterns = [
#    path('<int:pk>/', single_post_page),
#    path('', views.index),
#]


#CBV(Class Based View)일때
urlpatterns = [
    path('create_post/', views.PostCreate.as_view()),
    path('tag/<str:slug>/', views.tag_page),
    path('category/<str:slug>/', views.category_page),
    path('<int:pk>/', views.PostDetail.as_view()),
    path('', views.PostList.as_view()),
]

