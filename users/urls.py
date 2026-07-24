from django.urls import path, re_path
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from . import views

urlpatterns = [
    path('register/', views.UserRegistrationView.as_view(), name='user-register'),
    path('login/', views.LoginView.as_view(), name='user-login'),
    path('logout/', views.LogoutView.as_view(), name='user-logout'),
    path('profile/', views.UserProfileView.as_view(), name='user-profile'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change-password'),
    path('my-posts/', views.UserMyPostsView.as_view(), name='user-my-posts'),
    path('applications/', views.UserJobApplicationsView.as_view(), name='user-applications'),
    path('favorites/', views.FavoriteListCreateView.as_view(), name='favorites-list'),
    path('favorites/<int:pk>/', views.FavoriteDeleteView.as_view(), name='favorite-delete'),
    
    path('notifications/', views.NotificationListView.as_view(), name='notification-list'),
    path('notifications/<int:pk>/', views.NotificationUpdateView.as_view(), name='notification-update'),
    
    # Google OAuth
    re_path(r'^auth/google/?$', views.GoogleLoginView.as_view(), name='google-login'),
    
    # JWT Token
    path('auth/token/', TokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('auth/me/', views.CurrentUserView.as_view(), name='current-user'),
]
