from django.http import HttpResponse
from django.shortcuts import render

from .models import TracePoint

def index(request):
    return HttpResponse("Traces Index")

def entry(request):
    questions = TracePoint.objects.all()
    return render(request, 'traces/entry_form.html', { 'questions': questions })