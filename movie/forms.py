from django import forms
from django.contrib.auth import get_user_model

from movie.models import Actor, Movie, Director


class ActorForm(forms.ModelForm):
    movies = forms.ModelMultipleChoiceField(
        queryset=Movie.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Actor
        fields = "__all__"


class DirectorForm(forms.ModelForm):
    movies = forms.ModelMultipleChoiceField(
        queryset=Movie.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Director
        fields = ["bio", "first_name", "last_name", "age", "movies"]


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = "__all__"
