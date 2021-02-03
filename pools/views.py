from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse

from .models import Question, Choice, Voters

# Create your views here.
def home(request):
	return render(request,'pools/home.html')


def index(request):
	latest_question_list = Question.objects.order_by('-pub_date')[:5]
	context={'latest_question_list':latest_question_list}
	return render(request,'pools/index.html',context)
def detail(request, question_id):
	question = Question.objects.get(pk=question_id)
	#return HttpResponse("You're looking at question %s."%question_id)
	
	return render(request, 'pools/detail.html', {'question':question})

def results(request,question_id):
	question = get_object_or_404(Question, pk=question_id)
	return render(request,'pools/results.html', {'question':question})

def vote(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	try:
		selected_choice = question.choice_set.get(pk=request.POST['choice'])
	except (KeyError, Choice.DoesNotExist):
		return render(request,'pools/detail.html',{
			'question':question,
			'error_message':'Invalid choice.'
			})
	else:
		selected_choice.votes+=1
		selected_choice.save()
		return HttpResponseRedirect(reverse('pools:results', args=[question.id,]))

def voter(request):
	if request.method == "POST":
		voter_name = request.POST['VoterName']
		voter_id = request.POST['VoterId']
		votr = Voters.objects.create(voter_name=voter_name,voter_id=voter_id)
		votr.save();
		users = Voters.objects.all()
		return render(request,'pools/home.html',{'users':users})
	else:
		return render(request,'pools/people.html')
		

		
		
		
		

