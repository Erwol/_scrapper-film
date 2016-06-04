# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, request, response
from .models import *
# Create your views here.


def	inicio(request):
    return render(request, 'scrappy/index.html', {})


def resultados(request):
    print str(request.POST['nombre_peli'])
    if request.method == "POST":
        peli = request.POST['nombre_peli']
        if peli:
            print peli
            # Comprobamos si la peli está en nuestra BD
            res = Film.objects.filter(name=peli).count()
            if res == 1:
                # Si lo está, vemos cuándo fue consultada por última vez. Si han pasado menos de 24 horas desde la última
                # vez, tomamos las últimas puntuaciones de la BD. Si no, recalificamos.
                print "Hola"

                #call = Call.objects.get(password=request.POST['examKey'])
                # Añadimos como variable de sesión el id de la convocatoria
                # TODO: Añadir comprobación de la fecha del examen
                #request.session['call_id'] = call.id

                #return HttpResponseRedirect(reverse('users:registerStudent'))
            else:
                mensaje = "¡No pudimos encontrar la película " + str(peli) + "!"
                return render(request, 'scrappy/index.html', {
                    'error_message': mensaje,
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
"""""