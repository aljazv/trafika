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

    prodajno_mesto1 = ProdajnoMesto(ime = "Trafika Ljubljana", naslov = "Cankarjeva ulica 1", postna_stevilka = "1000", obcina = "Ljubljana", kontaktna_oseba = "Luka Cvek", telefon = "041456289")
    prodajno_mesto1.save()

    podjetje = Podjetje(ime = "trafika d.o.o.", naslov = "Škofja Loka 12", postna_stevilka = "4220", obcina = "Škofja Loka", davcna_stevilka = "67294308")
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
    #naredi potnika
    user, created = User.objects.get_or_create(username="potnik", email="potnik@gmail.com")
    user.first_name = "Jure"
    user.last_name = "Hovelja"

    if created:
        user.set_password("adminadmin")
        user.is_staff=True
        user.is_superuser=False
    
    user.save()

    potnik = Potnik(user = user, prodajno_mesto = prodajno_mesto, telefon = "031786453", email = "potnik@gmail.com")
    potnik.save()

    #
    uporabnik_admin = Uporabnik(user = user_admin, podjetje = podjetje, prodajno_mesto = prodajno_mesto)
    uporabnik_admin.save()

    skupina_izdelkov1 = SkupinaIzdelkov(ime = "Magneti", koda = "2389472983")
    skupina_izdelkov1.save()

    skupina_izdelkov2 = SkupinaIzdelkov(ime = "Razglednice", koda = "2734242398")
    skupina_izdelkov2.save()

    tag_bled = Tag(ime = "Bled")
    tag_bled.save()
    tag_slovenia = Tag(ime = "Slovenija")
    tag_slovenia.save()
    
    izdelek_bled = Izdelek(ime = "Magnet Bled", opis = "Dimenzija: 60x80mm", skupina_izdelkov = skupina_izdelkov1, koda = "AZU456B")
    
    izdelek_bled.slika.save('Bled.jpg', File(open(r'media/gallery/magneti_zbirno_201710.jpg','rb')))
    izdelek_bled.tag.add(tag_bled);
    izdelek_bled.tag.add(tag_slovenia);

    narocilo_bled = NarociloIzdelka(izdelek = izdelek_bled,kolicina = 25)
    narocilo_bled.save()

    izdelek_triglav = Izdelek(ime = "Magnet Triglav", opis = "Dimenzija: 60x80mm", skupina_izdelkov = skupina_izdelkov1, koda = "GHLO99S")
    izdelek_triglav.slika.save("Triglav.jpg", File(open(r'media/gallery/magneti_zbirno_201711.jpg','rb')))
    izdelek_triglav.tag.add(tag_slovenia);
    
    narocilo_triglav = NarociloIzdelka(izdelek = izdelek_triglav,kolicina = 100)
    narocilo_triglav.save()

    

    izdelek_razglednica1 = Izdelek(ime = "Razglednica test 1", opis = "Dimenzija: 60x80mm", skupina_izdelkov = skupina_izdelkov2, koda = "AZU4as356B")
    izdelek_razglednica1.slika.save("jama.jpg", File(open(r'media/gallery/mag_panoramski_11.jpg','rb')))
    narocilo_izdelek_razglednica1 = NarociloIzdelka(izdelek = izdelek_razglednica1,kolicina = 100)
    narocilo_izdelek_razglednica1.save()

    izdelek_razglednica2 = Izdelek(ime = "Razglednica test 2", opis = "Dimenzija: 60x80mm", skupina_izdelkov = skupina_izdelkov2, koda = "sadfasdf")
    izdelek_razglednica2.slika.save("marija.jpg", File(open(r'media/gallery/magneti_zbirno_201727.jpg','rb')))
    narocilo_izdelek_razglednica2 = NarociloIzdelka(izdelek = izdelek_razglednica2,kolicina = 100)
    narocilo_izdelek_razglednica2.save()

    kosarica = Kosarica(uporabnik = uporabnik_admin)
    kosarica.save()
    kosarica.narocila_izdelka.add(narocilo_bled,narocilo_triglav,narocilo_izdelek_razglednica1,narocilo_izdelek_razglednica2)
    kosarica.save()
