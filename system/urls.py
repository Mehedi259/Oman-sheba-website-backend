from django.urls import path
from . import views

urlpatterns = [
    path('sliders/', views.HeroSliderListView.as_view(), name='hero-slider-list'),
    path('search/', views.GlobalSearchView.as_view(), name='global-search'),
]
