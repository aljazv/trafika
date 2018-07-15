from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User

from .models import *
from .forms import *
from django.core.files import File
import os.path
import os


def naredi_bazo(request):
    #naredi uporabnika
    user_aljaz, created = User.objects.get_or_create(username="aljazrupar", email="aljazrupar@gmail.com")
    user_aljaz.first_name = "Aljaz"
    user_aljaz.last_name = "Rupar"

    if created:
        user_aljaz.set_password("adminadmin")
        user_aljaz.is_staff=False
        user_aljaz.is_superuser=False
    
    user_aljaz.save()

    uporabnik1 = Uporabnik(user = user_aljaz, podjetje = "siddarta", lastnik = "Janez Skok")
    uporabnik1.save()

    uporabnik1 = Uporabnik(user = User.objects.get(username='admin'), podjetje = "siddadrta", lastnik = "Jaasdnez Skok")
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
   
    uporabnik_admin = Uporabnik(user = user_admin, podjetje = "Alpin", lastnik = "Uroš")
    uporabnik_admin.save()

    skupina_izdelkov1 = SkupinaIzdelkov(ime = "Magneti")
    skupina_izdelkov1.save()

    tag_bled = Tag(ime = "Bled")
    tag_bled.save()
    
    izdelek_bled = Izdelek(ime = "Magnet Bled", opis = "Dimenzija: 60x80mm", skupina_izdelkov = skupina_izdelkov1, koda = "AZU456B")
    izdelek_bled.slika.save('Bled.jpg', File(open(r'media/gallery/Bled.jpg','rb')))
    narocilo_bled = NarociloIzdelka(izdelek = izdelek_bled,kolicina = 25)
    narocilo_bled.save()

    izdelek_triglav = Izdelek(ime = "Magnet Triglav", opis = "Dimenzija: 60x80mm", skupina_izdelkov = skupina_izdelkov1, koda = "GHLO99S")
    izdelek_triglav.slika.save("Triglav.jpg", File(open(r'media/gallery/Triglav.jpg','rb')))
    narocilo_triglav = NarociloIzdelka(izdelek = izdelek_triglav,kolicina = 100)
    narocilo_triglav.save()

    kosarica = Kosarica(uporabnik = uporabnik_admin)
    kosarica.save()
    kosarica.narocila_izdelka.add(narocilo_bled,narocilo_triglav)
    kosarica.save()
    