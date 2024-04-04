from django.contrib import admin
from .models import Calculation

@admin.register(Calculation)
class CalculationAdmin(admin.ModelAdmin):
    list_display = ('id', 'expression', 'result', 'status', 'created_at', 'started_at', 'finished_at')
    list_filter = ('status',)
    search_fields = ('expression', 'result')
