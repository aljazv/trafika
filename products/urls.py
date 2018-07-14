from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:index>/',views.index_skupina,name='index_skupina'),
    path('<int:index>/<str:search_string>',views.search,name='search')
]