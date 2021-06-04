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
    path('cinemas/<int:pk>/opinion', FilmOpinionCreateView.as_view(), name='filmopinion-create'),
    path('cinemas/<int:pk>/update', CinemaUpdateView.as_view(), name='cinema-update'),
    path('cinemas/<int:pk>/delete', CinemaDeleteView.as_view(), name='cinema-delete'),
    path('films/', views.films, name='films'),
    path('films/new/', FilmCreateView.as_view(), name='film-create'),
    path('films/<int:pk>/', FilmDetailView.as_view(), name='film-detail'),
    path('film/<int:pk>/update', FilmUpdateView.as_view(), name='film-update'),
    path('film/<int:pk>/delete', FilmDeleteView.as_view(), name='film-delete'),
    path('series/', views.series, name='series'),
    path('series/new/', SeriesCreateView.as_view(), name='series-create'),
    path('series/<int:pk>/', SeriesDetailView.as_view(), name='series-detail'),
    path('series/<int:pk>/update', SeriesUpdateView.as_view(), name='series-update'),
    path('series/<int:pk>/delete', SeriesDeleteView.as_view(), name='series-delete'),
    path('staff/', views.staff, name='staff'),
    path('staff/new/', StaffCreateView.as_view(), name='staff-create'),
    path('staff/<int:pk>/', StaffDetailView.as_view(), name='staff-detail'),
    path('staff/<int:pk>/update', StaffUpdateView.as_view(), name='staff-update'),
    path('staff/<int:pk>/delete', StaffDeleteView.as_view(), name='staff-delete'),
]
