from django.urls import path
from . import views

urlpatterns = (
    path('', views.home, name='mycinema-home'),
    path('about/', views.about, name='mycinema-about'),
)
