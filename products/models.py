from django.db import models
from django.contrib.auth.models import User, Group


class SkupinaIzdelkov(models.Model):
    ime = models.CharField(max_length=100, verbose_name="Ime skupine izdelkov")

    def __str__(self):
        return self.ime 

class Tag(models.Model):
    ime = models.CharField(max_length = 100, verbose_name="Ime taga(piši z malo)")

    def __str__(self):
        return self.ime 

class Izdelek(models.Model):
    ime = models.CharField(max_length=100, verbose_name="Ime izdelka")
    opis = models.TextField(max_length=300, verbose_name="Opis izdelka")
    slika = models.ImageField(upload_to="gallery", verbose_name= "Slika izdelka")
    skupina_izdelkov = models.ForeignKey(SkupinaIzdelkov,  null = True, on_delete=models.SET_NULL)
    tag = models.ManyToManyField(Tag)
    koda = models.CharField(max_length=100)

    zaloga = models.BooleanField(default=True, verbose_name="Ali je izdelek na zalogi")
    aktiven = models.BooleanField(default=True, verbose_name="Ali naj bo prikazan na strani")

    def __str__(self):
        return self.ime  



class NarociloIzdelka(models.Model):
    izdelek = models.ForeignKey(Izdelek, null = True, on_delete=models.SET_NULL)
    kolicina = models.IntegerField()



class Uporabnik(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    podjetje = models.CharField(max_length = 100)
    lastnik = models.CharField(max_length = 100)

class Narocilo(models.Model):

    uporabnik = models.ForeignKey(Uporabnik, on_delete=models.CASCADE)
    opomba = models.CharField(blank=True, max_length=200)
    # ce ne specificiras datuma se bo shranil trenutni datum
    datum = models.DateTimeField(auto_now=True, verbose_name="Datum naročila")
    narocila_izdelka = models.ManyToManyField(NarociloIzdelka)
    

    je_obdelan = models.BooleanField(default=False, verbose_name="Ali je naročilo že obdelano")

    def __str__(self):
        if self.je_obdelan:
            return "Staro narocilo: " + str(self.id)
        else:
            return "Novo narocilo: " + str(self.id)

#se mi zdi da je vseeno potrebno lociti kosarico od narocil, da ne bo uporabnika kej zmedlo
class Kosarica(models.Model):
    narocila_izdelka = models.ManyToManyField(NarociloIzdelka)
    uporabnik = models.ForeignKey(Uporabnik, on_delete=models.CASCADE)
