from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django_resized import ResizedImageField


# Create your models here.
class CommonInfo(models.Model):
    class Meta:
        abstract = True

    short_description = models.CharField(max_length=100, default="")
    main_description = models.TextField(blank=True)
    total_rating = models.IntegerField(default=0)
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


class News(CommonInfo):
    CATEGORY = (
        ('MOVIE', 'MOVIE'),
        ('TVSERIES', 'TVSERIES'),
        ('DIRECTORS', 'DIRECTORIES'),
        ('CINEMAS', 'CINEMAS'),
        ('ACTORS', 'ACTORS'),
        ('OTHERS', 'OTHERS')
    )

    title = models.CharField(max_length=100)
    category = models.CharField(max_length=50, null=True, choices=CATEGORY)
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('news-detail', kwargs={'pk': self.pk})




class Film(CommonInfo):
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
    title = models.CharField(max_length=100)
    genre = models.CharField(max_length=50, null=True, choices=GENRES)

    def __str__(self):
        return self.title


class Staff(CommonInfo):
    PROFESSIONS = (
        ('Actor', 'Actor'),
        ('Director', 'Director'),
        ('Producer', 'Producer'),
        ('Director of Photography', 'Director of Photography'),
        ('Costume Designer', 'Costume Designer'),
        ('Movie Editor', 'Movie Editor'),
        ('Composer', 'Composer')
    )
    name = models.CharField(max_length=100)
    profession = models.CharField(max_length=50, null=True, choices=PROFESSIONS)
    related_films = models.ManyToManyField(Film)

    def __str__(self):
        return self.name


class Cinema(CommonInfo):
    name = models.CharField(max_length=100)
    image = ResizedImageField(size=[256, 256], crop=['middle', 'center'],
                              quality=90, upload_to='cinema/', default='cinema/cinema_default.png')
    localization = models.CharField(max_length=60, default='Unknown')
    opening_hours = models.TextField(blank=True)
    #repertoire = models.ManyToManyField(Film)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('cinema-detail', kwargs={'pk': self.pk})

class Opinions(models.Model):
    RATINGS = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5)
    )
    authorek = models.ForeignKey(User, on_delete=models.CASCADE)

    opinion = models.TextField(blank=True)
    post = models.ForeignKey(News, related_name="opinionss", on_delete=models.CASCADE)
    #film = models.ForeignKey(Film, related_name="filmss", on_delete=models.CASCADE)
    #staff = models.ForeignKey(Staff, related_name="staffs", on_delete=models.CASCADE)
    #cinema = models.ForeignKey(Cinema, related_name="opinionss", on_delete=models.CASCADE)

    rating = models.IntegerField(choices=RATINGS)
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.opinion

    def get_absolute_url(self):
        return reverse('mycinema-home')
