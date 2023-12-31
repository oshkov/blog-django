from django.urls import path
from . import views 

urlpatterns = [
    path('', views.index),
    path('about/', views.about),
    path('addpost/', views.addPost),
    path('post<id>/', views.fullArticle),
    path('search=<search>/', views.indexSearch),
    path('edit<id>/', views.editPost),
]