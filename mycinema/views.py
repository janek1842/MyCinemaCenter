from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from .models import *
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse


# Create your views here.

def home(request):
    context = {
        'posts': News.objects.all()
    }

    return render(request, 'mycinema/home.html', context)


def cinemas(request):
    context = {
        'cinemas': Cinema.objects.all()
    }

    return render(request, 'mycinema/cinemas.html', context)


def about(request):
    return render(request, 'mycinema/about.html', {'title': 'Mytitle'})


class PostListView(ListView):
    model = News
    template_name = 'mycinema/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']


class PostDetailView(DetailView):
    model = News

    def form_valid(self, form):
        form.instance.authorek = self.request.user
        form.instance.post_id = self.kwargs['pk']
        return super().form_valid(form)


class OpinionCreateView(CreateView):
    model = Opinions
    template_name = 'mycinema/add_opinion.html'
    fields = ['opinion', 'rating']

    def form_valid(self, form):
        form.instance.authorek = self.request.user
        form.instance.post_id = self.kwargs['pk']
        return super().form_valid(form)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = News
    fields = ['title', 'short_description', 'main_description', 'category']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = News
    fields = ['title', 'short_description', 'main_description', 'category']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = News

    success_url = '/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class CinemaCreateView(LoginRequiredMixin, CreateView):
    model = Cinema
    fields = ['name', 'short_description', 'main_description']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class CinemaDetailView(DetailView):
    model = Cinema
