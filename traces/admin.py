from django.http import StreamingHttpResponse
from django.contrib import admin
from django.contrib.admin import DateFieldListFilter
from rangefilter.filter import DateRangeFilter
from .models import Question, Visit
from .exporter import Exporter

admin.site.register(Question)

def export_to_file(modeladmin, request, queryset):
    exporter = Exporter()
    response = StreamingHttpResponse(exporter.generate_rows(queryset),
                                     content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename="visit_list.csv"'
    return response
export_to_file.short_description = "Export visits to file"

class VisitAdmin(admin.ModelAdmin):
    list_filter = (
        ('date_created', DateFieldListFilter),
        ('date_created', DateRangeFilter)
    )

    actions = [export_to_file]

admin.site.register(Visit, VisitAdmin)