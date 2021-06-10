from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from .models import *
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse
from django.http import HttpResponseRedirect
from .forms import *


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


def addsub(request):
    if request.method == 'POST':
        if "subscribedid" in request.POST and "subscribedfilmid" in request.POST:
            idusera = request.POST['subscribedid']
            idfilmu = request.POST['subscribedfilmid']
            rodzaj = request.POST['rodzaj']

            user = User.objects.get(pk=idusera)

            if (rodzaj == "film"):
                film = Film.objects.get(pk=idfilmu)
            if (rodzaj == "series"):
                film = Series.objects.get(pk=idfilmu)
            if (rodzaj == "cinema"):
                film = Cinema.objects.get(pk=idfilmu)
            if (rodzaj == "staff"):
                film = Staff.objects.get(pk=idfilmu)

            film.subscribed_by.add(user)

    return render(request, 'mycinema/films.html')


def unsub(request):
    if request.method == 'POST':
        if "subscribedid" in request.POST and "subscribedfilmid" in request.POST:
            idusera = request.POST['subscribedid']
            idfilmu = request.POST['subscribedfilmid']
            rodzaj = request.POST['rodzaj']

            user = User.objects.get(pk=idusera)

            if (rodzaj == "film"):
                film = Film.objects.get(pk=idfilmu)
            if (rodzaj == "series"):
                film = Series.objects.get(pk=idfilmu)
            if (rodzaj == "cinema"):
                film = Cinema.objects.get(pk=idfilmu)
            if (rodzaj == "staff"):
                film = Staff.objects.get(pk=idfilmu)

            film.subscribed_by.remove(user)

    return render(request, 'mycinema/films.html')


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
    class Meta:
        abstract = True

    model = Opinion
    template_name = 'mycinema/add_opinion.html'
    fields = ['opinion', 'rating']

    def form_valid(self, form):
        form.instance.authorek = self.request.user
        form.instance.opinion_subject_id = self.kwargs['pk']
        return super().form_valid(form)


class NewsOpinionCreateView(OpinionCreateView):
    model = NewsOpinions


class FilmOpinionCreateView(OpinionCreateView):
    model = FilmOpinions


class CinemaOpinionCreateView(OpinionCreateView):
    model = CinemaOpinions


class StaffOpinionCreateView(OpinionCreateView):
    model = StaffOpinions


class SeriesOpinionCreateView(OpinionCreateView):
    model = SeriesOpinions


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


def mycinema(request):

    list = []

    list.extend(Staff.objects.filter(subscribed_by=request.user.id))
    list.extend(Cinema.objects.filter(subscribed_by=request.user.id))
    list.extend(Film.objects.filter(subscribed_by=request.user.id))
    list.extend(Series.objects.filter(subscribed_by=request.user.id))


    print(list)

    length = len(list)

    if length % 2 == 0:
        length /= 2
    else:
        length = (length + 1) / 2

    a = []
    b = []

    for i in range(len(list)):
        if i % 2 == 0:
            a.append(list[i])
        else:
            b.append(list[i])
    if len(a) > len(b):
        b.append(None)

    context = {
        'data': zip(a, b),
        'half_length': length
    }

    return render(request, 'mycinema/mycinema.html', context)


def ranking(request):
    data = []

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        films_form = FilmsRankingForm(request.POST)
        series_form = SeriesRankingForm(request.POST)
        staff_form = StaffRankingForm(request.POST)
        news_form = NewsRankingForm(request.POST)
        cinemas_form = CinemasRankingForm(request.POST)

        # check whether it's valid:
        if 'cinemas_form_btn' in request.POST and cinemas_form.is_valid():
            data.append('cinemas are here')

        if 'films_form_btn' in request.POST and films_form.is_valid():
            data.append('films are here')
            # process the data in form.cleaned_data as required

        if 'series_form_btn' in request.POST and series_form.is_valid():
            data.append('series are here')

        if 'staff_form_btn' in request.POST and staff_form.is_valid():
            data.append('staff are here')

        if 'news_form_btn' in request.POST and news_form.is_valid():
            data.append('news are here')


    else:
        # if a GET (or any other method) -> create a blank form
        films_form = FilmsRankingForm()
        series_form = SeriesRankingForm()
        staff_form = StaffRankingForm()
        news_form = NewsRankingForm()
        cinemas_form = CinemasRankingForm()

    context = {
        'films_form': films_form,
        'series_form': series_form,
        'staff_form': staff_form,
        'news_form': news_form,
        'cinemas_form': cinemas_form,
        'data': data
    }

    return render(request, 'mycinema/ranking.html', context)
