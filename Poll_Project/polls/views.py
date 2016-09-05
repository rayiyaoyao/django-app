from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
#3 from django.template import loader

from .models import Question

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

def index(request):
	latest_question_list = Question.objects.order_by('-pub_date')[:5]
	context = { 'latest_question_list': latest_question_list, }
	return render(request, 'polls/index.html', context)


#4 def detail(request, question_id):
#4 	return HttpResponse("You're looking at question %s." % question_id)

#5 def detail(request, question_id):
#5 	try:
#5 		question = Question.objects.get(pk = question_id)
#5 	except Question.DoesNotExist:
#5 		raise Http404("Question does not exist!")
#5 	return render(request, 'polls/detail.html', { 'question': question })

def detail(request, question_id):
	question = get_object_or_404(Question, pk = question_id)
	return render(request, 'polls/detail.html', { 'question': question })

def results(request, question_id):
	return HttpResponse("You're looking at the result of question %s." % question_id)

def vote(request, question_id):
	return HttpResponse("you're voting on question %s." %question_id)



























