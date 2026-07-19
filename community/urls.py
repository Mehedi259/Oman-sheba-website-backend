from django.urls import path
from . import views

urlpatterns = [
    path('posts/', views.PostListCreateView.as_view(), name='post-list'),
    path('posts/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    path('posts/<int:post_id>/comments/', views.CommentListCreateView.as_view(), name='post-comments'),
    path('posts/<int:post_id>/like/', views.PostLikeView.as_view(), name='post-like'),
    
    # Classifieds
    path('classifieds/', views.ClassifiedListCreateView.as_view(), name='classified-list'),
    path('classifieds/<int:pk>/', views.ClassifiedDetailView.as_view(), name='classified-detail'),
    path('classifieds/categories/', views.ClassifiedCategoryListView.as_view(), name='classified-category-list'),
    
    # Forum
    path('forum/posts/', views.ForumPostListCreateView.as_view(), name='forum-post-list'),
    path('forum/posts/<int:pk>/', views.ForumPostDetailView.as_view(), name='forum-post-detail'),
]
