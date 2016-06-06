# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

from django.db import models
from django.utils import timezone


class Origin(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    name = models.CharField(max_length=50, unique=True, blank=False)
    url = models.CharField(max_length=50, unique=True, blank=True)

    def __str__(self):
        return self.name


class Film(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=100, unique=False, blank=False)
    origin = models.ForeignKey(Origin, on_delete=models.CASCADE)
    last_score = models.FloatField()

    def __str__(self):
        return self.name + " de " + self.origin.name + "."


# Aquí guardamos un histórico de búsquedas
class Score(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    film = models.ForeignKey(Film, on_delete=models.CASCADE)
    origin = models.ForeignKey(Origin, on_delete=models.CASCADE)
    score = models.FloatField()

    def __str__(self):
        return str(self.score) + " " + str(self.film.name)
