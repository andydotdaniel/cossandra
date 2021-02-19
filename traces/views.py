from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, reverse

from .models import Question, Customer

def index(request):
    return render(request, 'traces/index.html')

def check(request):
    phone_number = request.POST['phone_number']
    try:
        customer = Customer.objects.get(pk=phone_number)
    except (KeyError, Customer.DoesNotExist):
        return HttpResponseRedirect(reverse('traces:entry') + '?phone_number=' + phone_number)
    else:
        return "Phone number found"

def entry(request):
    questions = Question.objects.all()
    context = {
        'questions': questions,
        'phone_number': request.GET['phone_number']
    }
    return render(request, 'traces/entry_form.html', context)