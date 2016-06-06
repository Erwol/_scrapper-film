# -*- coding: utf-8 -*-
from django.shortcuts import render
from .models import *
import filmaffinity
import fotogramas
import imdb
from django.utils.timezone import utc
from datetime import datetime
from threading import Thread


def	inicio(request):
    return render(request, 'scrappy/index.html', {})


def guarda_peliculas(listado, origen):
    for peli in listado:
        num_results = Film.objects.filter(name=peli[0], origin=origen).count()
        if num_results == 0:
            nueva_peli = Film(name=peli[0], origin=origen, last_score=peli[1])
            nueva_peli.save()
            nueva_puntuacion = Score(score=peli[1], film=nueva_peli, origin=origen)
            nueva_puntuacion.save()


# Función que busca en nuestra base de datos (que actúa como caché)
def busqueda_interna(peli):
    coincidencias = []
    nota = 0
    for pelicula in Film.objects.all():
        if str(peli).lower() in str(pelicula.name).lower():
            nota += pelicula.last_score
            coincidencias.append(pelicula)
    return coincidencias, nota


# Función que procesa la votación del usuario
def votar(request, film_id):
    # TODO Tratar de meter votaciones propias
    pelicula = Film.objects.get(film_id=film_id)
    pelicula.update()
    nota = request.POST['nota']
    #pelicula_id


# Listas globales para la configuración multithreading
l1 = []
l2 = []
l3 = []


def buscarF(p):
    global l1
    l1 = filmaffinity.buscar(p)


def buscarFoto(p):
    global l2
    l2 = fotogramas.buscar(p)


def buscarI(p):
    global l3
    l3 = imdb.buscar(p)


# Esta función actualiza añade nuevos registros de puntuaciones a la base de datos
def actualizar_puntuaciones(listado, origen):
    for pelicula in listado:
        pelicula_existente = Film.objects.get(name=pelicula[0], origin=origen)
        # Guardamos la puntuación sea o no igual a la última introducida para poder generar un histórico
        nueva_puntuacion = Score(score=pelicula[1], film=pelicula_existente, origin=origen)
        nueva_puntuacion.save()
        print (">Guardamos nueva puntuación (" + str(pelicula[1]) + ") de la película " + pelicula_existente.name + ".")

# Función que busca películas cuyo nombre esté contenido en la cadena peli en las webs abajo definidas
def busqueda_externa(request, peli, actualizando):
    p1 = Thread(target=buscarF, args=(peli,))
    p2 = Thread(target=buscarFoto, args=(peli,))
    p3 = Thread(target=buscarI, args=(peli,))

    p1.start()
    p2.start()
    p3.start()

    p1.join()
    p2.join()
    p3.join()

    # Si en ninguno de los orígenes se ha encontrado nuestra búsqueda, devolvemos un mensaje de error
    if not l1 and not l2 and not l3:
        return False # Si no se ha encontrado la pelicula, corta la ejecución y en el programa que llama a esta soltamos la excepción

    # La primera vez que se guardan estas películas en la BD
    if not actualizando:
        if l1:
            guarda_peliculas(l1, Origin.objects.get(name="filmaffinity"))
        if l2:
            guarda_peliculas(l2, Origin.objects.get(name="fotogramas"))
        if l3:
            guarda_peliculas(l3, Origin.objects.get(name="imdb"))
    else:
        if l1:
            actualizar_puntuaciones(l1, Origin.objects.get(name="filmaffinity"))
        if l2:
            actualizar_puntuaciones(l2, Origin.objects.get(name="fotogramas"))
        if l3:
            actualizar_puntuaciones(l3, Origin.objects.get(name="imdb"))
    return True


# Función que determina si hay que refrescar o no la información relacionada con una película desde un origen externo
def refrescar(listado):
    for peli in listado:
        # Volveremos a busccar las películas si han pasado esos segundos
        if (datetime.utcnow().replace(tzinfo=utc) - peli.updated_at).total_seconds() > 60 * 60 * 24:
            print (">La película " + peli.name + " fue actualizada por última vez el " + str(peli.updated_at) + " y hay que actualizarla porque ha transcurrido el tiempo estipulado.")
            return True




# Función que procesa la búsqueda efectuada por el usuario
def resultados(request):
    if request.method == "POST":
        forzar = request.POST.get('forzar') # Objeto multvaluado. Devolverá True o False
        peli = request.POST['nombre_peli']
        if peli:
            coincidencias, nota = busqueda_interna(peli)
            if coincidencias and not forzar:   # Hay al menos una entrada que coincide con un texto introducido
                if refrescar(coincidencias):
                    # Como ha pasado un tiempo desde que comprobamos en el exterior, refrescamos la BD
                    if not busqueda_externa(request, peli, True):
                        mensaje = "¡No pudimos encontrar la película " + str(peli) + " en ninguna de nuestras fuentes!"
                        return render(request, 'scrappy/index.html', {
                            'error_message': mensaje,
                        })
                    coincidencias, nota = busqueda_interna(peli)
                    if nota == 0:
                        media = 0
                    else:
                        media = format(nota / len(coincidencias), '.2f')
                    return render(request, 'scrappy/index.html', {
                        'peliculas': coincidencias,
                        'peli': peli,
                        'media': media,
                    })
                else:
                    if nota == 0:
                        media = 0
                    else:
                        media = format(nota / len(coincidencias), '.2f')
                    return render(request, 'scrappy/index.html', {
                        'peliculas': coincidencias,
                        'peli': peli,
                        'media': media,
                    })
            else:
                print ("Sin coincidencias en la BD para " + peli)
                if not busqueda_externa(request, peli, False):
                    mensaje = "¡No pudimos encontrar la película " + str(peli) + " en ninguna de nuestras fuentes!"
                    return render(request, 'scrappy/index.html', {
                        'error_message': mensaje,
                    })
                coincidencias, nota = busqueda_interna(peli)
                if nota == 0:
                    media = 0
                else:
                    media = format(nota / len(coincidencias), '.2f')
                return render(request, 'scrappy/index.html', {
                    'peliculas': coincidencias,
                    'peli': peli,
                    'media': media,
                })
        else:
            return render(request, 'scrappy/index.htmk', {
                'error_message': "Algo extraño pasó.",
            })
    else:
        return render(request, 'scrappy/index.html', {})
