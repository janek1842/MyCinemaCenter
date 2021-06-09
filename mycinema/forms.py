from django import forms
from .models import GENRES, PROFESSIONS, CATEGORY


class RankingForm(forms.Form):
    class Meta:
        abstract = True

    SELECTING_METHOD = (
        ('TR', 'Top rated'),
        ('MC', 'Most commented'),
    )

    method = forms.ChoiceField(label="Sorting by:", choices=SELECTING_METHOD)
    items_number = forms.IntegerField(label='Numbers of items', min_value=1)


class NewsRankingForm(RankingForm):
    category = forms.ChoiceField(label='Category', choices=CATEGORY)


class FilmsRankingForm(RankingForm):
    genres = forms.ChoiceField(label='Genres', choices=GENRES)


class SeriesRankingForm(RankingForm):
    series_genres = forms.ChoiceField(label='Genres', choices=GENRES)


class StaffRankingForm(RankingForm):
    professions = forms.ChoiceField(label='Professions', choices=PROFESSIONS)


class CinemasRankingForm(RankingForm):
    hidden = forms.HiddenInput()
