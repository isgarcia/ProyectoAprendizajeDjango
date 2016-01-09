# coding: utf-8

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from polls.models import *

# Create your views here.
def index(request):
	latest_question_list = Question.objects.order_by('-pub_date')[:5]
	context = {
		'latest_question_list' : latest_question_list
	}
	return render(request,'index.html', context)
	#output = ', '.join([p.question_text for p in latest_question_list])
	#return HttpResponse(output)

	#return HttpResponse('Hola mundo esto es una aplicacion django')

def detail(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	context = {
		'question' : question
	}
	return render(request, 'detail.html', context)
	#return HttpResponse('Ahora mismo estas mirando la pregunta ' + question_id)

def detailJSON(self,question_id):
	question = get_object_or_404(Question, pk=question_id)
	context = {
		'question' : question
	}
	return HttpResponse(question.toJSON(), content_type='application/json')

def results(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	context = {
		'question' : question
	}
	return render(request, 'results.html' , context)
	#return HttpResponse('Estas viendo los resultados de ' + question_id)

def vote(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	try:
		selected_choice = question.choice_set.get(pk=request.POST['choice'])
	except (KeyError, Choice.DoesNotExist):
		context = {
			'question' : question,
			'error_message' : 'No has seleccionado ninguna opcion',
		}
		return render(request, 'detail.html', context)
	else:
		if 'votes' in request.session:
			request.session['votes'].append(question.id)
		else:
			request.session['votes'] = [question.id]

		request.session.modified = True #fuerza a django para actualizar la informacion de sesion del usuario

		selected_choice.votes += 1
		selected_choice.save()
		return HttpResponseRedirect(reverse('results', args=(question.id,)))
	#return HttpResponse('Estas votando en ' + question_id)