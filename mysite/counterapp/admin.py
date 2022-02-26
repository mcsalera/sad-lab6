from typing import Counter
from django.contrib import admin
from .models import Counter


# Register your models here.
class CounterAdmin(admin.ModelAdmin):
    list_display = ('name', 'value',)


admin.site.register(Counter, CounterAdmin)
