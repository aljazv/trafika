from django.urls import path

from . import views

urlpatterns = [
    path('', views.nova_narocila, name='nova_narocila')
]