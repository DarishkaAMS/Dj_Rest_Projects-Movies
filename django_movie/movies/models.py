from django.db import models
from datetime import date

from django.urls import reverse


class Category(models.Model):
    """Categories"""
    name = models.CharField("category", max_length=150)
    description = models.TextField("description")
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"


class Actor(models.Model):
    """Actors & Directors"""
    name = models.CharField("name", max_length=100)
    age = models.PositiveSmallIntegerField("age", default=0)
    description = models.TextField("description")
    image = models.ImageField("picture", upload_to="actors/")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('actor_detail', kwargs={"slug": self.name})

    class Meta:
        verbose_name = "actor_director"
        verbose_name_plural = "actors_directors"


class Genre(models.Model):
    """Genres"""
    name = models.CharField("name", max_length=100)
    description = models.TextField("description")
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "genre"
        verbose_name_plural = "genres"


class Movie(models.Model):
    """Movie"""
    title = models.CharField("title", max_length=100)
    tagline = models.CharField("tagline", max_length=100, default='')
    description = models.TextField("description")
    poster = models.ImageField("poster", upload_to="movies/")
    year = models.PositiveSmallIntegerField("Year", default=2019)
    country = models.CharField("country", max_length=30)
    directors = models.ManyToManyField(Actor, verbose_name="director", related_name="film_director")
    actors = models.ManyToManyField(Actor, verbose_name="actors", related_name="film_actor")
    genres = models.ManyToManyField(Genre, verbose_name="genres")
    world_premiere = models.DateField("world_premiere", default=date.today)
    budget = models.PositiveIntegerField("budget", default=0,
                                         help_text="indicate in USD")
    fees_in_usa = models.PositiveIntegerField(
        "fees_in_usa", default=0, help_text="indicate in USD"
    )
    fess_in_world = models.PositiveIntegerField(
        "fees_in_world", default=0, help_text="indicate in USD"
    )
    category = models.ForeignKey(
        Category, verbose_name="category", on_delete=models.SET_NULL, null=True
    )
    url = models.SlugField(max_length=130, unique=True)
    draft = models.BooleanField("draft", default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("movie_detail", kwargs={"slug": self.url})

    def get_review(self):
        return self.reviews_set.filter(parent__isnull=True)

    class Meta:
        verbose_name = "movie"
        verbose_name_plural = "movies"


class MovieShots(models.Model):
    """Movie Shots"""
    title = models.CharField("title", max_length=100)
    description = models.TextField("description")
    image = models.ImageField("picture", upload_to="movie_shots/")
    movie = models.ForeignKey(Movie, verbose_name="movie", on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "movie_shot"
        verbose_name_plural = "movie_shot"


class RatingStar(models.Model):
    """Rating Star"""
    value = models.SmallIntegerField("value", default=0)

    def __str__(self):
        return f'{self.value}'

    class Meta:
        verbose_name = "rating_star"
        verbose_name_plural = "rating_star"
        ordering = ["-value"]


class Rating(models.Model):
    """Rating"""
    ip = models.CharField("ip_address", max_length=15)
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE, verbose_name="star")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name="movie", related_name="ratings")

    def __str__(self):
        return f"{self.star} - {self.movie}"

    class Meta:
        verbose_name = "rating"
        verbose_name_plural = "ratings"


class Review(models.Model):
    """Review"""
    email = models.EmailField()
    name = models.CharField("name", max_length=100)
    text = models.TextField("text", max_length=5000)
    parent = models.ForeignKey(
        'self', verbose_name="parent", on_delete=models.SET_NULL, blank=True, null=True
    )
    movie = models.ForeignKey(Movie, verbose_name="movie", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.movie}"

    class Meta:
        verbose_name = "review"
        verbose_name_plural = "reviews"
