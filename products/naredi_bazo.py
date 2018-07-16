from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User

from .models import *
from .forms import *
from django.core.files import File
import os.path
import os


def naredi_bazo(request):

    prodajno_mesto = ProdajnoMesto(ime = "Trafika Škofja Loka", naslov = "Škofja Loka 88", postna_stevilka = "4220", obcina = "Škofja Loka", kontaktna_oseba = "Anja Novak", telefon = "041500677")
    prodajno_mesto.save()

    podjetje = Podjetje(podjetje = "trafika d.o.o.", naslov = "Škofja Loka 12", postna_stevilka = "4220", obcina = "Škofja Loka", davcna_stevilka = "67294308")
    podjetje.save()

    uporabnik1 = Uporabnik(user = User.objects.get(username='admin'), podjetje = podjetje, prodajno_mesto = prodajno_mesto)
    uporabnik1.save()

    #naredi admina
    user_admin, created = User.objects.get_or_create(username="adminadmin", email="admin@gmail.com")
    user_admin.first_name = "admin"
    user_admin.last_name = "admin"

    if created:
        user_admin.set_password("adminadmin")
        user_admin.is_staff=True
        user_admin.is_superuser=True
    
    user_admin.save()
   
    uporabnik_admin = Uporabnik(user = user_admin, podjetje = podjetje, prodajno_mesto = prodajno_mesto)
    uporabnik_admin.save()

    skupina_izdelkov1 = SkupinaIzdelkov(ime = "Magneti", koda = "238947298347")
    skupina_izdelkov1.save()

    tag_bled = Tag(ime = "Bled")
    tag_bled.save()
    
    izdelek_bled = Izdelek(ime = "Magnet Bled", opis = "Dimenzija: 60x80mm", skupina_izdelkov = skupina_izdelkov1, koda = "AZU456B")
    izdelek_bled.slika.save('Bled.jpg', File(open(r'media/gallery/magneti_zbirno_201710.jpg','rb')))
    narocilo_bled = NarociloIzdelka(izdelek = izdelek_bled,kolicina = 25)
    narocilo_bled.save()

    izdelek_triglav = Izdelek(ime = "Magnet Triglav", opis = "Dimenzija: 60x80mm", skupina_izdelkov = skupina_izdelkov1, koda = "GHLO99S")
    izdelek_triglav.slika.save("Triglav.jpg", File(open(r'media/gallery/magneti_zbirno_201711.jpg','rb')))
    narocilo_triglav = NarociloIzdelka(izdelek = izdelek_triglav,kolicina = 100)
    narocilo_triglav.save()

    kosarica = Kosarica(uporabnik = uporabnik_admin)
    kosarica.save()
    kosarica.narocila_izdelka.add(narocilo_bled,narocilo_triglav)
    kosarica.save()
    