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


def kosarica(request):
	#tle bo se za spremenit ko bo LOGIN delal-------------------------------------------------
	#dela ker je sam ena kosrica ustvarjena!
	#Za popraviti sumnike
	#plus se dimenzije slik
	if request.method == 'POST' and 'odstrani_izdelek' in request.POST:
		narocilo_izdelka_id = request.POST['narocilo']
		narocilo_izdelka = NarociloIzdelka.objects.filter(id = narocilo_izdelka_id)
		narocilo_izdelka.delete()
	if request.method == 'POST' and 'spremeni_kolicino' in request.POST:
		kolicina = request.POST['kolicina']
		narocilo_izdelka_id = request.POST['narocilo']
		narocilo_izdelka = NarociloIzdelka.objects.filter(id = narocilo_izdelka_id)[0]
		narocilo_izdelka.kolicina = kolicina
		narocilo_izdelka.save()

	kosarica_uporabnika = Kosarica.objects.all()[0]
	narocila_izdelkov = kosarica_uporabnika.narocila_izdelka.all()

	context = {
		'arr': narocila_izdelkov
		}

	return render(request,'products/kosarica.html',context)

def pregled_narocil(request):

	return HttpResponse(status=201)