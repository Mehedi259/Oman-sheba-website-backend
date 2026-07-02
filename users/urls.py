from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.UserRegistrationView.as_view(), name='user-register'),
    path('login/', views.LoginView.as_view(), name='user-login'),
    path('logout/', views.LogoutView.as_view(), name='user-logout'),
    path('profile/', views.UserProfileView.as_view(), name='user-profile'),
    path('favorites/', views.FavoriteListCreateView.as_view(), name='favorites-list'),
    path('favorites/<int:pk>/', views.FavoriteDeleteView.as_view(), name='favorite-delete'),
]
