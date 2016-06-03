# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone


# Create your models here.
class Film(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    name = models.CharField(max_length=100, unique=True, blank=False)

    def __str__(self):
        return self.name


class Origin(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    name = models.CharField(max_length=50, unique=False, blank=False)

    def __str__(self):
        return self.name


class Score(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    film = models.ForeignKey(Film, on_delete=models.CASCADE)
    origin = models.ForeignKey(Origin, on_delete=models.CASCADE)
    score = models.IntegerField()

    def __str__(self):
        return self.score, " a la película ", self.film.name, " el ", self.created_at, "."
