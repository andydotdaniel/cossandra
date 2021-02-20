import csv
from .models import Question

class Echo:
    """An object that implements just the write method of the file-like
    interface.
    """
    def write(self, value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value

class Exporter:
    def __get_headers(self):
        headers = ["phone_number", "group_size"]
        questions = Question.objects.all()
        for question in questions:
            headers.append(question.name)

        return headers

    def __format_row(self, queryset):
        row = [
            queryset.customer.phone_number,
            queryset.group_size
        ]

        entry_inputs = queryset.customer.entry_set.all()
        for entry_input in entry_inputs:
            row.append(entry_input.value)

        return row

    def generate_rows(self, queryset):
        """A view that streams a large CSV file."""
        pseudo_buffer = Echo()
        writer = csv.writer(pseudo_buffer)

        yield writer.writerow(self.__get_headers())

        for query in queryset:
            yield writer.writerow(self.__format_row(query))