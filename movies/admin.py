from django.contrib import admin

from .models import Movie


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "genre",
        "release_year",
        "personal_rating",
        "watched",
        "date_added",
    )
    list_filter = ("watched", "genre")
    search_fields = ("title",)
    list_editable = ("watched",)
    ordering = ("-date_added",)
