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
    length = Cinema.objects.count()
    if length % 2 == 0:
        length /= 2
    else:
        length = (length + 1) / 2

    a = []
    b = []
    cinemas_list = Cinema.objects.all()
    for i in range(len(cinemas_list)):
        if i % 2 == 0:
            a.append(cinemas_list[i])
        else:
            b.append(cinemas_list[i])
    if len(a) > len(b):
        b.append(None)

    context = {
        'cinemas': zip(a, b),
        'half_length': length
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
    fields = ['name', 'localization', 'opening_hours', 'main_description', 'image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_initial(self, *args, **kwargs):
        initial = super(CinemaCreateView, self).get_initial(**kwargs)
        initial['localization'] = ''
        return initial

class CinemaDetailView(DetailView):
    model = Cinema

class CinemaUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Cinema
    fields = CinemaCreateView.fields

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class CinemaDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Cinema

    success_url = '/cinemas'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
