from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic

from movie.forms import ActorForm, DirectorForm, MovieForm, ReviewForm, SignupForm
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
    model = Actor
    fields = "__all__"
    paginate_by = 5


class MovieListView(generic.ListView):
    model = Movie
    fields = "__all__"
    paginate_by = 10


class DirectorListView(generic.ListView):
    model = Director
    fields = "__all__"
    paginate_by = 5


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
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.creator = request.user
            review.film = movie
            review.save()
            return redirect('movies:movie_detail', pk=movie.id)
    else:
        form = ReviewForm()
    return render(request, "movie/add_review.html", {'form': form, 'movie': movie})


def sign_up(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = SignupForm()
    return render(request, 'registration/signup.html', {'form': form})


class UserDetailView(generic.DetailView):
    model = User
    fields = ("username", "first_name", "last_name",)


@login_required
def toggle_add_to_favourites(request, pk):
    user = User.objects.get(id=request.user.id)
    movie = Movie.objects.get(id=pk)
    if movie in user.favourite_movies.all():
        user.favourite_movies.remove(movie)
    else:
        user.favourite_movies.add(movie)
    return HttpResponseRedirect(reverse_lazy("movies:movie_detail", args=[pk]))
