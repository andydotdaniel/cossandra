from django.contrib import admin

from .models import Question, Visit

admin.site.register(Question)
admin.site.register(Visit)