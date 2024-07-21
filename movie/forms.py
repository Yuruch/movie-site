from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from movie.models import (
    Actor,
    Movie,
    Director,
    Review,
    Genre
)


class ActorForm(forms.ModelForm):
    movies = forms.ModelMultipleChoiceField(
        queryset=Movie.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Actor
        fields = ("first_name", "last_name", "bio", "age", "movies", "photo")


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
    genres = forms.ModelMultipleChoiceField(
        queryset=Genre.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    directors = forms.ModelMultipleChoiceField(
        queryset=Director.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    actors = forms.ModelMultipleChoiceField(
        queryset=Actor.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Movie
        fields = "__all__"


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text="*")
    profile_pic = forms.ImageField(required=False)

    class Meta:
        model = get_user_model()
        fields = ("username", "email", "password1", "password2")


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(
        max_length=200,
        required=False
    )
    profile_pic = forms.ImageField(required=False)

    class Meta:
        model = get_user_model()
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "profile_pic"
        )


class MovieSearchForm(forms.Form):
    title = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "Search by title"}
        )
    )
    genre = forms.ModelChoiceField(
        queryset=Genre.objects.all(),
        label="Genres",
        widget=forms.RadioSelect,
        required=False
    )


class ActorSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "Search by name"}
        )
    )


class DirectorSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "Search by name"}
        )
    )
