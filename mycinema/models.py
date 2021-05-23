from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


# Create your models here.

class News(models.Model):
    CATEGORY = (
        ('MOVIE', 'MOVIE'),
        ('TVSERIES', 'TVSERIES'),
        ('DIRECTORS', 'DIRECTORIES'),
        ('CINEMAS', 'CINEMAS'),
        ('ACTORS', 'ACTORS'),
        ('OTHERS', 'OTHERS')
    )

    title = models.CharField(max_length=100)
    # tagi ? kogo lub czego dotyczy dany news
    category = models.CharField(max_length=50, null=True, choices=CATEGORY)
    # kategoria której dotyczy news-> film,serial,kino,reżyserzy etc.
    date_posted = models.DateTimeField(default=timezone.now)
    short_description = models.CharField(max_length=100)
    main_description = models.TextField(blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('news-detail', kwargs = {'pk': self.pk})
