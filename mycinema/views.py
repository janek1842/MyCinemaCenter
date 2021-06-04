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


class FilmOpinionCreateView(CreateView):
    model = FilmOpinions
    template_name = 'mycinema/add_opinion.html'
    fields = ['opinion', 'rating']

    def form_valid(self, form):
        form.instance.authorek = self.request.user
        form.instance.filmpost_id = self.kwargs['pk']
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


class FilmCreateView(LoginRequiredMixin, CreateView):
    model = Film
    fields = ['title', 'genre', 'short_description', 'main_description', 'image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_initial(self, *args, **kwargs):
        initial = super(FilmCreateView, self).get_initial()
        initial['localization'] = ''
        return initial


class FilmDetailView(DetailView):
    model = Film


class FilmUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Film
    fields = FilmCreateView.fields

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class FilmDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Film
    success_url = '/films'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def films(request):
    length = Film.objects.count()
    if length % 2 == 0:
        length /= 2
    else:
        length = (length + 1) / 2

    a = []
    b = []
    films_list = Film.objects.all()
    for i in range(len(films_list)):
        if i % 2 == 0:
            a.append(films_list[i])
        else:
            b.append(films_list[i])
    if len(a) > len(b):
        b.append(None)

    context = {
        'films': zip(a, b),
        'half_length': length
    }

    return render(request, 'mycinema/films.html', context)


class SeriesCreateView(LoginRequiredMixin, CreateView):
    model = Series
    fields = ['title', 'genre', 'short_description', 'main_description', 'image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_initial(self, *args, **kwargs):
        initial = super(SeriesCreateView, self).get_initial()
        initial['localization'] = ''
        return initial


class SeriesDetailView(DetailView):
    model = Series


class SeriesUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Series
    fields = SeriesCreateView.fields

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class SeriesDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Series
    success_url = '/series'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def series(request):
    length = Series.objects.count()
    if length % 2 == 0:
        length /= 2
    else:
        length = (length + 1) / 2

    a = []
    b = []
    series_list = Series.objects.all()
    for i in range(len(series_list)):
        if i % 2 == 0:
            a.append(series_list[i])
        else:
            b.append(series_list[i])
    if len(a) > len(b):
        b.append(None)

    context = {
        'series': zip(a, b),
        'half_length': length
    }

    return render(request, 'mycinema/series.html', context)


class StaffCreateView(LoginRequiredMixin, CreateView):
    model = Staff
    fields = ['name', 'profession', 'image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_initial(self, *args, **kwargs):
        initial = super(StaffCreateView, self).get_initial()
        initial['localization'] = ''
        return initial


class StaffDetailView(DetailView):
    model = Staff


class StaffUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Staff
    fields = StaffCreateView.fields

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class StaffDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Staff
    success_url = '/staff'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def staff(request):
    length = Staff.objects.count()
    if length % 2 == 0:
        length /= 2
    else:
        length = (length + 1) / 2

    a = []
    b = []
    staff_list = Staff.objects.all()
    for i in range(len(staff_list)):
        if i % 2 == 0:
            a.append(staff_list[i])
        else:
            b.append(staff_list[i])
    if len(a) > len(b):
        b.append(None)

    context = {
        'staff': zip(a, b),
        'half_length': length
    }

    return render(request, 'mycinema/staff.html', context)
