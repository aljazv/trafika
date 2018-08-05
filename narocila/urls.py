from django.urls import path

from . import views, excel

urlpatterns = [
    path('nova_narocila/', views.nova_narocila, name='nova_narocila'),
    path('nova_narocila/<int:id>/', views.spremeni, name='spremeni'),
    path('stara_narocila/', views.stara_narocila, name='stara_narocila'),
    path('statistika/', excel.prenesi_xls, name='statistika')
]