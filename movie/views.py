from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch, Avg
from django.db.models.functions import Round
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseRedirect
)
from django.shortcuts import (
    render,
    get_object_or_404,
    redirect
)
from django.urls import reverse_lazy
from django.views import generic

from movie.forms import (
    ActorForm,
    DirectorForm,
    MovieForm,
    ReviewForm,
    SignUpForm,
    UserUpdateForm,
    MovieSearchForm,
    ActorSearchForm,
    DirectorSearchForm
)
from movie.models import (
    Movie,
    Actor,
    Director,
    Review,
    User
)
from movie.services import movies


def index(request: HttpRequest) -> HttpResponse:
    num_movies = Movie.objects.count()
    num_actors = Actor.objects.count()
    num_directors = Director.objects.count()
    best_movies = movies.best_movies(16)
    context = {
        "num_movies": num_movies,
        "num_actors": num_actors,
        "num_directors": num_directors,
        "best_movies": best_movies,
    }
    if request.user.is_authenticated:
        movies_you_like = movies.movie_you_like(request.user, 16)
        context["movies_you_like"] = movies_you_like
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
            queryset = queryset.filter(
                first_name__icontains=form.cleaned_data["name"]
            )
        orderby = self.request.GET.get("orderby")
        if orderby == "name":
            queryset = queryset.order_by("first_name")
        elif orderby == "surname":
            queryset = queryset.order_by("last_name")
        elif orderby == "age":
            queryset = queryset.order_by("-age")
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
        context["orderby"] = self.request.GET.get("orderby", "")
        return context

    def get_queryset(self):
        queryset = Movie.objects.prefetch_related(
            "reviews"
        ).annotate(
            avg_rating=Round(Avg("reviews__rating"), 2)
        )

        form = MovieSearchForm(self.request.GET)
        if form.is_valid():
            if form.cleaned_data["title"]:
                queryset = queryset.filter(
                    title__icontains=form.cleaned_data["title"]
                )
            if form.cleaned_data["genre"]:
                queryset = queryset.filter(genres=form.cleaned_data["genre"])

        orderby = self.request.GET.get("orderby")
        if orderby == "title":
            queryset = queryset.order_by("title")
        elif orderby == "rating":
            queryset = queryset.order_by("-avg_rating")

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
            queryset = queryset.filter(
                first_name__icontains=form.cleaned_data["name"]
            )
        orderby = self.request.GET.get("orderby")
        if orderby == "name":
            queryset = queryset.order_by("first_name")
        elif orderby == "surname":
            queryset = queryset.order_by("last_name")
        elif orderby == "age":
            queryset = queryset.order_by("-age")
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
            "directors",
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
            context["is_favourite"] = user.favourite_movies.filter(
                id=self.object.id
            ).exists()
        else:
            context["is_favourite"] = False
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

    def get_initial(self):
        initial = super().get_initial()
        initial["movies"] = self.object.movies.all()
        return initial

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

    def get_initial(self):
        initial = super().get_initial()
        initial["movies"] = self.object.movies.all()
        return initial

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

    def get_success_url(self):
        return reverse_lazy(
            "movies:movie_detail",
            kwargs={"pk": self.object.pk}
        )


def add_review(request: HttpRequest, pk: int) -> HttpResponse:
    movie = get_object_or_404(Movie, pk=pk)
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.creator = request.user
            review.movie = movie
            review.save()
            return redirect("movies:movie_detail", pk=movie.id)
    else:
        form = ReviewForm()
    return render(
        request,
        "movie/review_form.html",
        {"form": form, "movie": movie}
    )


def update_review(
        request: HttpRequest,
        movie_pk: int,
        review_pk: int
) -> HttpResponse:
    movie = get_object_or_404(Movie, pk=movie_pk)
    review = get_object_or_404(Review, pk=review_pk, creator=request.user)

    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect("movies:movie_detail", pk=movie.pk)
    else:
        form = ReviewForm(instance=review)

    return render(
        request,
        "movie/review_form.html",
        {"form": form, "movie": movie}
    )


def delete_review(
        request: HttpRequest,
        movie_pk: int,
        review_pk: int
) -> HttpResponse:
    movie = get_object_or_404(Movie, pk=movie_pk)
    review = get_object_or_404(Review, pk=review_pk, creator=request.user)

    if request.method == "POST":
        review.delete()
        return redirect("movies:movie_detail", pk=movie.pk)

    return render(
        request,
        "movie/review_confirm_delete.html",
        {"review": review, "movie": movie}
    )


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


class MovieDeleteView(generic.DeleteView):
    model = Movie
    success_url = reverse_lazy("movies:movie_list")


class ActorDeleteView(generic.DeleteView):
    model = Actor
    success_url = reverse_lazy("movies:actor_list")


class DirectorDeleteView(generic.DeleteView):
    model = Director
    success_url = reverse_lazy("movies:directors_list")
