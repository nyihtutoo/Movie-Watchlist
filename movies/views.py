from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import MovieForm
from .models import Movie


def movie_list(request):
    """Homepage: list all movies (newest first) with title search."""
    query = request.GET.get("q", "").strip()
    movies = Movie.objects.all()  # Meta.ordering already sorts newest first
    if query:
        movies = movies.filter(Q(title__icontains=query))
    context = {"movies": movies, "query": query}
    return render(request, "movies/movie_list.html", context)


def movie_create(request):
    """Add a new movie."""
    if request.method == "POST":
        form = MovieForm(request.POST)
        if form.is_valid():
            movie = form.save()
            messages.success(request, f'"{movie.title}" was added to your watchlist.')
            return redirect("movies:movie_list")
    else:
        form = MovieForm()
    context = {"form": form, "title": "Add Movie"}
    return render(request, "movies/movie_form.html", context)


def movie_update(request, pk):
    """Edit an existing movie."""
    movie = get_object_or_404(Movie, pk=pk)
    if request.method == "POST":
        form = MovieForm(request.POST, instance=movie)
        if form.is_valid():
            form.save()
            messages.success(request, f'"{movie.title}" was updated.')
            return redirect("movies:movie_list")
    else:
        form = MovieForm(instance=movie)
    context = {"form": form, "title": "Edit Movie", "movie": movie}
    return render(request, "movies/movie_form.html", context)


def movie_delete(request, pk):
    """Delete a movie (confirmation on GET, delete on POST)."""
    movie = get_object_or_404(Movie, pk=pk)
    if request.method == "POST":
        title = movie.title
        movie.delete()
        messages.success(request, f'"{title}" was removed from your watchlist.')
        return redirect("movies:movie_list")
    context = {"movie": movie}
    return render(request, "movies/movie_confirm_delete.html", context)


def movie_toggle_watched(request, pk):
    """Mark a movie as Watched or Unwatched."""
    movie = get_object_or_404(Movie, pk=pk)
    if request.method == "POST":
        movie.watched = not movie.watched
        movie.save(update_fields=["watched"])
        state = "watched" if movie.watched else "unwatched"
        messages.success(request, f'"{movie.title}" marked as {state}.')
    return redirect("movies:movie_list")
