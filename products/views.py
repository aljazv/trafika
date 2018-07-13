from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator
from django.template import loader
from django.shortcuts import render
import datetime

from .models import *
from .forms import *


#context: opozorilo je za display informacij


#index je glavna stran ki si prikaze ko se uporabnik prijavi
# na njej so ZAENKRAT VSI izdelki
def index(request):
    if request.method == 'POST':
        #print(request.POST)
        return HttpResponse("Ni takega dsasaddselementa")
        kolicina_form = KolicinaForm(request.POST)

        if kolicina_form.is_valid():

            pass
        
    else:
        vsi_izdelki = Izdelek.objects.all().order_by('ime')
        vse_skupine = SkupinaIzdelkov.objects.all()


        #paginacija
        paginator = Paginator(vsi_izdelki, 25)
        page = request.GET.get('page')
        paginirani_izdelki = paginator.get_page(page)

        kolicina_form = KolicinaForm()


        context = {
            'opozorilo' : 'nic',
            'skupine': vse_skupine,
            'kolicina_form' : kolicina_form,
            'izdelki' : paginirani_izdelki,
            
        }

        return render(request,'products/index.html',context)


        
