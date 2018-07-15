from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
	path('kosarica/', views.kosarica, name='kosarica'),
	path('pregled_narocil/', views.pregled_narocil, name='pregled_narocil'),
    path('<int:index>/',views.index_skupina,name='index_skupina'),
    path('<int:index>/<str:search_string>',views.search,name='search')
]