from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic

from movie.forms import ActorForm, DirectorForm, MovieForm, ReviewForm, SignUpForm, UserUpdateForm, MovieSearchForm, \
    ActorSearchForm, DirectorSearchForm
from movie.models import Movie, Actor, Director, Review, User


# TODO add permissions


def index(request: HttpRequest) -> HttpResponse:
    num_movies = Movie.objects.count()
    num_actors = Actor.objects.count()
    num_directors = Director.objects.count()
    context = {
        "num_movies": num_movies,
        "num_actors": num_actors,
        "num_directors": num_directors,
    }
    return render(request, "movie/index.html", context)


def user_logout(request):
    logout(request)
    return render(request, "registration/logged_out.html")


class ActorListView(generic.ListView):
    fields = "__all__"
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = ActorSearchForm(
            initial={"name": name}
        )
        return context

    def get_queryset(self):
        queryset = Actor.objects.all()
        form = ActorSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(
                first_name__icontains=form.cleaned_data["name"]
            )
        return queryset


class MovieListView(generic.ListView):
    fields = "__all__"
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        title = self.request.GET.get("title", "")
        genre_id = self.request.GET.get("genre")
        context["search_form"] = MovieSearchForm(
            initial={"title": title, "genre": genre_id}
        )
        return context

    def get_queryset(self):
        queryset = Movie.objects.all()
        form = MovieSearchForm(self.request.GET)
        if form.is_valid():
            if form.cleaned_data["title"]:
                queryset = queryset.filter(title__icontains=form.cleaned_data["title"])
            if form.cleaned_data["genre"]:
                queryset = queryset.filter(genres=form.cleaned_data["genre"])
        return queryset


class DirectorListView(generic.ListView):
    fields = "__all__"
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = DirectorSearchForm(
            initial={"name": name}
        )
        return context

    def get_queryset(self):
        queryset = Director.objects.all()
        form = DirectorSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(
                first_name__icontains=form.cleaned_data["name"]
            )
        return queryset


class ActorDetailView(generic.DetailView):
    model = Actor
    fields = "__all__"
    queryset = Actor.objects.prefetch_related("movies")


class DirectorDetailView(generic.DetailView):
    model = Director
    fields = "__all__"
    queryset = Director.objects.prefetch_related("movies")


class MovieDetailView(generic.DetailView):
    model = Movie
    fields = "__all__"

    def get_queryset(self):
        return Movie.objects.prefetch_related(
            "director",
            "genres",
            "actors",
            Prefetch(
                "reviews",
                queryset=Review.objects.select_related("creator")
            )
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_authenticated:
            context['is_favourite'] = user.favourite_movies.filter(id=self.object.id).exists()
        else:
            context['is_favourite'] = False
        return context


class ActorCreateView(generic.CreateView):
    model = Actor
    form_class = ActorForm
    success_url = reverse_lazy("movies:actor_list")

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.movies.set(form.cleaned_data["movies"])
        return response


class ActorUpdateView(generic.UpdateView):
    model = Actor
    form_class = ActorForm
    success_url = reverse_lazy("movies:actor_list")

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.movies.set(form.cleaned_data["movies"])
        return response


class DirectorCreateView(generic.CreateView):
    model = Director
    form_class = DirectorForm
    success_url = reverse_lazy("movies:directors_list")

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.movies.set(form.cleaned_data["movies"])
        return response


class DirectorUpdateView(generic.UpdateView):
    model = Director
    form_class = DirectorForm
    success_url = reverse_lazy("movies:directors_list")

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.movies.set(form.cleaned_data["movies"])
        return response


class MovieCreateView(generic.CreateView):
    model = Movie
    form_class = MovieForm
    success_url = reverse_lazy("movies:movie_list")


class MovieUpdateView(generic.UpdateView):
    model = Movie
    form_class = MovieForm
    success_url = reverse_lazy("movies:movie_list")


def add_review(request: HttpRequest, pk: int) -> HttpResponse:
    movie = get_object_or_404(Movie, pk=pk)
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.creator = request.user
            review.film = movie
            review.save()
            return redirect("movies:movie_detail", pk=movie.id)
    else:
        form = ReviewForm()
    return render(request, "movie/add_review.html", {"form": form, "movie": movie})


def sign_up(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = SignUpForm()
    return render(request, "registration/signup.html", {"form": form})


def user_detail_view(request, pk):
    user = get_object_or_404(User, pk=pk)

    if request.user.id == user.id:
        return render(request, "movie/user_detail.html", {"user": user})
    else:
        return render(request, "movie/user_public.html", {"user": user})


@login_required
def toggle_add_to_favourites(request, pk):
    user = User.objects.get(id=request.user.id)
    movie = Movie.objects.get(id=pk)
    if movie in user.favourite_movies.all():
        user.favourite_movies.remove(movie)
    else:
        user.favourite_movies.add(movie)
    return HttpResponseRedirect(reverse_lazy("movies:movie_detail", args=[pk]))


class UserUpdateView(generic.UpdateView):
    model = User
    form_class = UserUpdateForm
    success_url = reverse_lazy("movies:home")
