from django.views import generic
from .models import Counter
from django.shortcuts import render
from django.db.models import F


class CounterView(generic.View):

    def get(self, request, *args, **kwargs):
        counter = Counter.objects.first()
        context = {}
        if counter:
            context = {
                'value': counter.value
            }
        return render(request, 'counterapp/counter.html', context)

def add_counter(request):
    counter = Counter.objects.first()
    context = {}
    
    if counter:
        counter.value = F('value') + 1
        counter.save(update_fields=['value'])
        counter.refresh_from_db()
        context = {
            'value': counter.value
        }
    
    return render(request, 'counterapp/counter.html', context)


def reset_counter(request):
    counter = Counter.objects.first()
    context = {}

    if counter:
        counter.value = 0
        counter.save(update_fields=['value'])
        counter.refresh_from_db()
        context = {
            'value': counter.value
        }
    
    return render(request, 'counterapp/counter.html', context)


