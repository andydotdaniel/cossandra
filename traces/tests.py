from django.test import TestCase, TransactionTestCase
from django.shortcuts import reverse
from django.utils import timezone

from .models import Customer, Visit, Question, Entry

class CustomerCheckTests(TestCase):
    def test_new_customer(self):
        """
        Given a check request, when new customer, then should be redirected to entry endpoint
        """
        data = {
            'phone_number': '08128881122',
            'group_size': 3
        }

        response = self.client.post(reverse('traces:check'), data)

        phone_number_param = 'phone_number=' + data['phone_number']
        group_size_param = 'group_size=' + str(data['group_size'])
        expected_url = reverse('traces:entry') + '?' + phone_number_param + '&' + group_size_param
        self.assertRedirects(response, expected_url, status_code=302)

    def test_returning_customer(self):
        """
        Given a check request, when returning customer, then should save new visit and redirect to welcome view
        """
        previous_visit_count = Visit.objects.all().count()

        group_size = 3
        phone_number = '08128881122'
        customer = Customer(phone_number=phone_number, date_created=timezone.now())
        customer.save()
        response = self.client.post(reverse('traces:check'), { 'phone_number': phone_number, 'group_size': group_size })

        self.assertRedirects(response, reverse('traces:welcome'), status_code=302)

        visits = Visit.objects.all().reverse()
        self.assertEqual(visits.count(), previous_visit_count + 1)
        self.assertEqual(visits[0].group_size, group_size)
        self.assertEqual(visits[0].customer, customer)

    def test_key_error(self):
        """
        Given a check request with an invalid key error, then should show error message in check form view
        """
        response = self.client.post(reverse('traces:check'), { 'invalid_key': '08128881122', 'group_size': 0 })
        self.assertContains(response, "So sorry! Something happened. Please try again.")

class IndexViewTests(TestCase):
    def test_show_view(self):
        """
        Given the request, then should show the view
        """
        response = self.client.get(reverse('traces:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Please enter your phone number")
        self.assertContains(response, "please do type in the number of people you come with")

class EntryFormTests(TransactionTestCase):
    def test_save_entry(self):
        """
        Given the entry post request, then should save the entry data for the new customer 
        """
        previous_customer_count = Customer.objects.all().count()
        previous_entry_count = Entry.objects.all().count()
        
        question = Question(name="email", input_title="Email", input_type=Question.FieldInputType.EMAIL)
        question.save()

        data = {
            'phone_number': '08128881122',
            'group_size': 3,
            question.name: "some@email.com"
        }

        response = self.client.post(reverse('traces:entry'), data)
        self.assertRedirects(response, reverse('traces:welcome'), status_code=302)

        entries = Entry.objects.all().reverse()
        self.assertEqual(entries.count(), previous_entry_count + 1)
        self.assertEqual(entries[0].customer.phone_number, data['phone_number'])
        self.assertEqual(entries[0].question, question)

        customers = Customer.objects.all().reverse()
        self.assertEqual(customers.count(), previous_customer_count + 1)
        self.assertEqual(customers[0].phone_number,  data['phone_number'])

    def test_save_entry_when_duplicate(self):
        """
        Given the entry post request with duplicate phone number, then should redirect to welcome view
        """

        phone_number = '08128881122'
        customer = Customer(phone_number=phone_number, date_created=timezone.now())
        customer.save()

        data = {
            'phone_number': phone_number,
            'group_size': 3,
        }

        response = self.client.post(reverse('traces:entry'), data)
        self.assertRedirects(response, reverse('traces:welcome'), status_code=302)

class EntryFormViewTests(TestCase):
    def test_show_view(self):
        """
        Given the request, then should show the view with query parameter values
        """
        phone_number = '08128881122'
        group_size = str(2)
        phone_number_param = 'phone_number=' + phone_number
        group_size_param = 'group_size=' + group_size

        response = self.client.get(reverse('traces:entry') + '?' + phone_number_param + '&' + group_size_param)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, phone_number)
        self.assertContains(response,  'name="group_size" value="' + group_size + '"')