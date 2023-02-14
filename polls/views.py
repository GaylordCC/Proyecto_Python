from asyncio.windows_events import NULL
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.http import Http404
from django.http import JsonResponse

from .models import Question, Choice

def index(request):
    #latest_question_list= Question.objects.all()
    latest_question_list= Question.objects.filter(pub_date__lte = timezone.now()).order_by("-pub_date")[:5]
    return render(request, "polls/index.html", {
        "latest_question_list": latest_question_list
    })


def detail(request, question_id):
    #return HttpResponse(f"Estas viendo la pregunta número {question_id}")
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/detail.html", {
        "question":question
    } )

def get_queryset(request, question_id):
    """
    Excludes any question that arent published yed
    """
    question = get_object_or_404(Question, pk=100, pub_date__lte = timezone.now())
    if not question:
       raise Http404("No MyModel matches the given query.")
       
    else:
      return  JsonResponse(status=404, data={})
    

def results(request, question_id):
    return HttpResponse(f"Estas viendo los resultados de la pregunta número {question_id}")


def vote(request, question_id):
    #return HttpResponse(f"Estas votando a la pregunta número {question_id}")
    question= get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(request, "polls/detail.html", {
            "question": question,
            "error_message": "No elesgiste una respuesta"
        })
    else:
        selected_choice.votes +=1
        selected_choice.save()
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))



