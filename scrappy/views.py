# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, request, response
from .models import *
import filmaffinity
import fotogramas
import imdb
# Necesario para buscar de forma concurrente en distintos origenes a la par
from multiprocessing import Pool, cpu_count, Process



def	inicio(request):
    return render(request, 'scrappy/index.html', {})

def analiza_pelicula(listado, origen):
    for peli in listado:
        num_results = Film.objects.filter(name=peli[0]).count()
        print ("Buscando película " + str(peli[0]) + ". " + str(num_results) + " resultados actualmente.")
        if num_results == 0:
            nueva_peli = Film(name=peli[0], origin=origen, last_score=peli[1])
            nueva_peli.save()
            nueva_puntuacion = Score(score=peli[1], film=nueva_peli, origin=origen)
            nueva_puntuacion.save()


def busca_coincidencias(peli):
    coincidencias = []
    nota = 0
    for pelicula in Film.objects.all():
        print ("Comparando >" + pelicula.name + "< con >" + str(peli) + "<")
        if str(peli).lower() in str(pelicula.name).lower():
            print ("Coincidencia de " + str(peli) + " con " + pelicula.name + ".")
            nota += pelicula.last_score
            coincidencias.append(pelicula)
    return coincidencias, nota


def resultados(request):
    if request.method == "POST":
        peli = request.POST['nombre_peli']
        if peli:
            coincidencias, nota = busca_coincidencias(peli)
            if coincidencias:   # Hay al menos una entrada que coincide con un texto introducido
                return render(request, 'scrappy/index.html', {
                    'peliculas': coincidencias,
                    'peli': peli,
                    'media': nota / len(coincidencias),
                })
            else:
                # Mejorar con concurrencia
                todas = []
                p1 = filmaffinity.buscar(peli)
                p2 = fotogramas.buscar(peli)
                p3 = imdb.buscar(peli)

                if not p1 and not p2 and not p3:
                    mensaje = "¡No pudimos encontrar la película " + str(peli) + " en ninguna de nuestras fuentes!"
                    return render(request, 'scrappy/index.html', {
                        'error_message': mensaje,
                    })

                if p1:
                    analiza_pelicula(p1, Origin.objects.get(name="filmaffinity"))
                    todas.append(p1)
                if p2:
                    analiza_pelicula(p2, Origin.objects.get(name="fotogramas"))
                    todas.append(p2)
                if p3:
                    analiza_pelicula(p3, Origin.objects.get(name="imdb"))
                    todas.append(p3)

                coincidencias, nota = busca_coincidencias(peli)
                return render(request, 'scrappy/index.html', {
                    'peliculas': coincidencias,
                    'peli': peli,
                    'media': nota / len(coincidencias),
                })

        else:
            return render(request, 'scrappy/index.htmk', {
                'error_message': "Algo extraño pasó.",
            })
    else:
        return render(request, 'scrappy/index.html', {})







"""""
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

    #return HttpResponseRedirect(reverse('users:registerStudent'))
"""""