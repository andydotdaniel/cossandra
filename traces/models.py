from django.db import models

class Customer(models.Model):
    phone_number = models.CharField(max_length=200, unique=True)
    date_created = models.DateTimeField()

class Question(models.Model):
    name = models.CharField(max_length=200, unique=True)
    input_title = models.CharField(max_length=200)

    def __str__(self):
        return self.input_title

class Entry(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.RESTRICT)
    value = models.CharField(max_length=200)

    def __str__(self):
        return self.value

class Visit(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date_created = models.DateTimeField()