from django.urls import path

from . import views

urlpatterns = [
    path('nova_narocila/', views.nova_narocila, name='nova_narocila'),
    path('stara_narocila/', views.stara_narocila, name='stara_narocila'),
]