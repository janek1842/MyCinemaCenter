from itertools import count

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django_resized import ResizedImageField

# predefined data -------------------------------------------
CATEGORY = (
    ('MOVIE', 'MOVIE'),
    ('TVSERIES', 'TVSERIES'),
    ('DIRECTORS', 'DIRECTORIES'),
    ('CINEMAS', 'CINEMAS'),
    ('ACTORS', 'ACTORS'),
    ('OTHERS', 'OTHERS')
)

GENRES = (
    ('Action', 'Action'),
    ('Adventure', 'Adventure'),
    ('Comedy', 'Comedy'),
    ('Crime', 'Crime'),
    ('Fantasy', 'Fantasy'),
    ('Historical', 'Historical'),
    ('Horror', 'Horror'),
    ('Musical', 'Musical'),
    ('Romance', 'Romance'),
    ('Science Fiction', 'Science Fiction'),
    ('Thriller', 'Thriller'),
    ('Western', 'Western'),
)

PROFESSIONS = (
    ('Actor', 'Actor'),
    ('Director', 'Director'),
    ('Producer', 'Producer'),
    ('Director of Photography', 'Director of Photography'),
    ('Costume Designer', 'Costume Designer'),
    ('Movie Editor', 'Movie Editor'),
    ('Composer', 'Composer')
)

RATINGS = (
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5)
)


# ----------------------------------------------------------------

# Create your models here.
class CommonInfo(models.Model):
    class Meta:
        abstract = True

    short_description = models.CharField(max_length=100, default="")
    main_description = models.TextField(blank=True)
    total_rating = models.FloatField(default=0)
    is_accepted = models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete=models.RESTRICT)
    moderator = models.CharField(max_length=50, default="-")
    opinion_counter = models.IntegerField(default=0)

    def handle_rating(self, new_rating):
        total = self.opinion_counter * self.total_rating
        self.opinion_counter += 1
        self.total_rating = (total + new_rating) / self.opinion_counter

    def __str__(self):
        return self.id

    def get_total_rate(self):
        self.total_rating = 0
        iteratore = 0
        for op in self.opinions.all():
            self.total_rating = self.total_rating + op.rating
            iteratore = iteratore + 1
        if iteratore != 0:
            return self.total_rating / iteratore
        else:
            return 0


class News(CommonInfo):
    title = models.CharField(max_length=100)
    category = models.CharField(max_length=50, null=True, choices=CATEGORY)
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('news-detail', kwargs={'pk': self.pk})


class Film(CommonInfo):
    title = models.CharField(max_length=100)
    genre = models.CharField(max_length=50, null=True, choices=GENRES)
    image = ResizedImageField(size=[256, 256], crop=['middle', 'center'],
                              quality=90, upload_to='film/', default='film/film_default.png')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('film-detail', kwargs={'pk': self.pk})


class Series(CommonInfo):
    title = models.CharField(max_length=100)
    genre = models.CharField(max_length=50, null=True, choices=GENRES)
    image = ResizedImageField(size=[256, 256], crop=['middle', 'center'],
                              quality=90, upload_to='series/', default='series/series_default.png')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('series-detail', kwargs={'pk': self.pk})


class Staff(CommonInfo):
    name = models.CharField(max_length=100)
    profession = models.CharField(max_length=50, null=True, choices=PROFESSIONS)
    image = ResizedImageField(size=[256, 256], crop=['middle', 'center'],
                              quality=90, upload_to='cinema/', default='staff/staff_default.png')
    related_films = models.ManyToManyField(Film)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('staff-detail', kwargs={'pk': self.pk})


class Cinema(CommonInfo):
    name = models.CharField(max_length=100)
    image = ResizedImageField(size=[256, 256], crop=['middle', 'center'],
                              quality=90, upload_to='cinema/', default='cinema/cinema_default.png')
    localization = models.CharField(max_length=60, default='Unknown')
    opening_hours = models.TextField(blank=True)

    # repertoire = models.ManyToManyField(Film)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('cinema-detail', kwargs={'pk': self.pk})


class Opinion(models.Model):
    class Meta:
        abstract = True

    authorek = models.ForeignKey(User, on_delete=models.CASCADE)
    opinion = models.TextField(blank=True)
    rating = models.IntegerField(choices=RATINGS)
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.opinion

    def get_absolute_url(self):
        return reverse('mycinema-home')


class NewsOpinions(Opinion):
    opinion_subject = models.ForeignKey(News, related_name="opinions", on_delete=models.CASCADE)


class FilmOpinions(Opinion):
    opinion_subject = models.ForeignKey(Film, related_name="opinions", on_delete=models.CASCADE)


class StaffOpinions(Opinion):
    opinion_subject = models.ForeignKey(Staff, related_name="opinions", on_delete=models.CASCADE)


class SeriesOpinions(Opinion):
    opinion_subject = models.ForeignKey(Series, related_name="opinions", on_delete=models.CASCADE)


class CinemaOpinions(Opinion):
    opinion_subject = models.ForeignKey(Cinema, related_name="opinions", on_delete=models.CASCADE)
