from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render, reverse

from .models import Question, Customer, Entry, Visit

def index(request):
    return render(request, 'traces/index.html')

def check(request):
    phone_number = request.POST['phone_number']
    try:
        customer = Customer.objects.get(phone_number=phone_number)
    except (KeyError, Customer.DoesNotExist):
        return HttpResponseRedirect(reverse('traces:entry') + '?phone_number=' + phone_number)
    else:
        visit = Visit(customer=customer, date_created=timezone.now())
        visit.save()
        return HttpResponseRedirect(reverse('traces:welcome'))

def entry(request):
    if request.method == 'POST':
        return __saveEntry(request)
    elif request.method == 'GET':
        return __showEntryForm(request)
    else:
        raise Http404

def __saveEntry(request):
    now = timezone.now()
    customer = Customer(phone_number=request.POST['phone_number'], date_created=now)
    customer.save()

    questions = Question.objects.all()
    for question in questions:
        entry = Entry(customer=customer, question=question, value=request.POST[question.name])
        entry.save()

    visit = Visit(customer=customer, date_created=now)
    visit.save()

    return HttpResponseRedirect(reverse('traces:welcome'))

def __showEntryForm(request):
    questions = Question.objects.all()
    context = {
        'questions': questions,
        'phone_number': request.GET['phone_number']
    }
    return render(request, 'traces/entry_form.html', context)

def welcome(request):
    return render(request, 'traces/welcome.html')