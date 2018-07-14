from django.http import HttpResponse, HttpResponseRedirect,JsonResponse , HttpResponseForbidden
from django.core.paginator import Paginator
from django.template import loader
from django.shortcuts import render
import datetime

from .models import *
from .forms import *


#context: opozorilo je za display informacij


#index je glavna stran ki si prikaze ko se uporabnik prijavi
#ce gres na main page te preusmeri na prvo skupino izdelkov
def index(request):

    prva_skupina = SkupinaIzdelkov.objects.first().id

    return HttpResponseRedirect(str(prva_skupina)+ "/")

#index_skupina je 
# na njej je skupina izdelkov izdelki
def index_skupina(request, index, search_string = None):

    #dodajanje izdelkov v koscarico
    if request.method == 'POST':
        print(request.user)
        print(request.POST)
        print(request.POST['kolicina'])

        if request.user.is_authenticated:
            
            uporabnik = Uporabnik.objects.get(user=request.user)

            if Kosarica.objects.filter(uporabnik=uporabnik).exists():
                kosarica_uporabnika = Kosarica.objects.get(uporabnik=uporabnik)
            else:
                kosarica_uporabnika = Kosarica(uporabnik=uporabnik)
                kosarica_uporabnika.save()


            

            kolicina = request.POST['kolicina']
            id_izdelka = request.POST['id_izdelka']

            izdelek = Izdelek.objects.get(id=id_izdelka)
            
            # ce narocilo za izdelek ze obstaja mu pristejemo stevilo kolicina
            if kosarica_uporabnika.narocila_izdelka.filter(izdelek=izdelek).exists():
                narocilo = kosarica_uporabnika.narocila_izdelka.get(izdelek=izdelek)
                narocilo.kolicina += int(kolicina)
                narocilo.save()
            #drugace naredimo novo narocilo izdelka
            else:
                nov_izdelek_za_kosarico = NarociloIzdelka(izdelek=izdelek, kolicina= kolicina)
                nov_izdelek_za_kosarico.save()
                kosarica_uporabnika.narocila_izdelka.add(nov_izdelek_za_kosarico)

            
            
            return JsonResponse({'success':'Izdelek dodan v košarico'}, status=200)
        else:
            return JsonResponse({'alert':'Napaka pri dodajanju'}, status=403)

        
    #prikaz izdelkov    
    else:

        if search_string != None:
            vsi_izdelki = Izdelek.objects.filter(tag__ime__istartswith=search_string)
            
        else:
            vsi_izdelki = Izdelek.objects.filter(aktiven=True).order_by('ime')
        
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

# vrne izdelke ki se ujemajo v tagu s search_stringom
def search(request, index , search_string):
    
    
    return index_skupina(request,index,search_string=search_string)

