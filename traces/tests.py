from django.test import TestCase
from django.shortcuts import reverse
from django.utils import timezone

from .models import Customer, Visit

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

class IndexViewTests(TestCase):
    def test_show_view(self):
        """
        Given the request, then should show the view
        """
        response = self.client.get(reverse('traces:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Please enter your phone number")
        self.assertContains(response, "please do type in the number of people you come with")