from django.http import HttpResponse
from django.shortcuts import render

from .models import Question

def index(request):
    return HttpResponse("Traces Index")

def entry(request):
    questions = Question.objects.all()
    context = {
        'questions': questions,
        'phone_number': request.GET['phone_number']
    }
    return render(request, 'traces/entry_form.html', context)