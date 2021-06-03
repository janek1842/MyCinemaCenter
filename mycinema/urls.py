from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', PostListView.as_view(), name='mycinema-home'),
    path('news/<int:pk>/', PostDetailView.as_view(), name='news-detail'),
    path('news/new/', PostCreateView.as_view(), name='news-create'),
    path('news/<int:pk>/opinion/', OpinionCreateView.as_view(), name='opinion-create'),
    path('news/<int:pk>/update', PostUpdateView.as_view(), name='news-update'),
    path('news/<int:pk>/delete', PostDeleteView.as_view(), name='news-delete'),
    path('about/', views.about, name='mycinema-about'),
    path('cinemas/', views.cinemas, name='cinemas'),
    path('cinemas/new/', CinemaCreateView.as_view(), name='cinema-create'),
    path('cinemas/<int:pk>/', CinemaDetailView.as_view(), name='cinema-detail'),
    path('cinemas/<int:pk>/update', CinemaUpdateView.as_view(), name='cinema-update'),
    path('cinemas/<int:pk>/delete', CinemaDeleteView.as_view(), name='cinema-delete')
]
