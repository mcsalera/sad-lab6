from django.urls import path, re_path
from . import views
from django.views.generic.base import TemplateView


app_name = 'counterapp'
urlpatterns = [
    path('', TemplateView.as_view(template_name='counterapp/index.html'), name='home'),
    re_path(r'^counter/', views.CounterView.as_view(), name='counter'),
    re_path(r'^add_counter', views.add_counter, name='add_counter'),
    re_path(r'^reset_counter', views.reset_counter, name='reset_counter')
]
