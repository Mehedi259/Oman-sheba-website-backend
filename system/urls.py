from django.urls import path
from . import views

urlpatterns = [
    path('sliders/', views.HeroSliderListView.as_view(), name='hero-slider-list'),
]
