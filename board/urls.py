from django.urls import path
from . import views

#FBV(Function Based view)일때
#urlpatterns = [
#    path('<int:pk>/', single_post_page),
#    path('', views.index),
#]


#CBV(Class Based View)일때
urlpatterns = [
    path('create/', views.BoardCreate.as_view()),
    path('<int:pk>/', views.BoardDetail.as_view()),
    path('', views.BoardList.as_view()),
]

