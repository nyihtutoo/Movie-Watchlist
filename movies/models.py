from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Movie(models.Model):
    """A single movie entry in the personal watchlist."""

    title = models.CharField(max_length=200)
    genre = models.CharField(max_length=100, blank=True)
    release_year = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1888), MaxValueValidator(2100)],
        help_text="Year the movie was released.",
    )
    personal_rating = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Your personal rating from 1 to 5.",
    )
    watched = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Homepage requirement: newest first.
        ordering = ["-date_added"]

    def __str__(self):
        return self.title
