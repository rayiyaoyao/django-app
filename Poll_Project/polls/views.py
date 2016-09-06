from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
#3 from django.template import loader

from .models import Question, Choice

#1 def index(request):
#1 	return HttpResponse("Hello, world! You are at the polls index.")

#2 def index(request):
#2 	latest_question_list = Question.objects.order_by('-pub_date')[:5]
#2 	output = ', '.join(q.question_text for q in latest_question_list)
#2 	return HttpResponse(output)

#3 def index(request):
#3 	latest_question_list = Question.objects.order_by('-pub_date')[:5]
#3 	template = loader.get_template('polls/index.html')
#3 	context = { 'latest_question_list': latest_question_list, }
#3 	return HttpResponse(template.render(context, request))

#8 def index(request):
#8 	latest_question_list = Question.objects.order_by('-pub_date')[:5]
#8 	context = {'latest_question_list': latest_question_list }
#8 	return render(request, 'polls/index.html', context)

class IndexView(generic.ListView):
	template_name = 'polls/index.html'
	context_object_name = 'latest_question_list'

	def get_queryset(self):
		return Question.objects.order_by('-pub_date')[:5]

#4 def detail(request, question_id):
#4 	return HttpResponse("You're looking at question %s." % question_id)

#5 def detail(request, question_id):
#5 	try:
#5 		question = Question.objects.get(pk = question_id)
#5 	except Question.DoesNotExist:
#5 		raise Http404("Question does not exist!")
#5 	return render(request, 'polls/detail.html', { 'question': question })

#8 def detail(request, question_id):
#8 	question = get_object_or_404(Question, pk = question_id)
#8 	return render(request, 'polls/detail.html', { 'question': question })

class DetailView(generic.DetailView):
	model = Question
	template_name = 'polls/detail.html'

#7 def results(request, question_id):
#7 	return HttpResponse("You're looking at the result of question %s." % question_id)

#8 def results(request, question_id):
#8 	question = get_object_or_404(Question, pk = question_id)
#8 	return render(request, 'polls/results.html', { 'question': question })

class ResultsView(generic.DetailView):
	model = Question
	template_name = 'polls/results.html'


#6 def vote(request, question_id):
#6 	return HttpResponse("you're voting on question %s." %question_id)


def vote(request, question_id):
	question = get_object_or_404(Question, pk = question_id)
	try:
		selected_choice = question.choice_set.get(pk = request.POST['choice'])
	except(KeyError, Choice.DoesNotExist):
		return render(request, 'polls/detail.html', { 
			'question': question, 'error_message':"You didn't select a choice.", })
	else:
		selected_choice.votes += 1
		selected_choice.save()
		return HttpResponseRedirect(reverse('polls:results', args = (question_id,)))

























