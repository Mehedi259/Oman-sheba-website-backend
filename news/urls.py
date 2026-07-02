from django.urls import path
from . import views

urlpatterns = [
    path('', views.NewsListView.as_view(), name='news-list'),
    path('<slug:slug>/', views.NewsDetailView.as_view(), name='news-detail'),
    path('<slug:slug>/comments/', views.NewsCommentListCreateView.as_view(), name='news-comments'),
]
