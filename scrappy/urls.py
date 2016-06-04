# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views


# ¡Da reverse match error si no, y hay que incluirlo en el urls de la app no del proyecto!
app_name = 'scrappy'
urlpatterns = [
    url(r'^$', views.inicio, name='inicio'),
    url(r'^buscarPelicula/', views.resultados, name='buscarPeli'),
]