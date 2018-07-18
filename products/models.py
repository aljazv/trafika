from django.db import models
from django.contrib.auth.models import User, Group
from imagekit.models import ImageSpecField 
from imagekit.processors import ResizeToFill 



class SkupinaIzdelkov(models.Model):
    ime = models.CharField(max_length=100, verbose_name="Ime skupine izdelkov")
    koda = models.CharField(max_length=100, verbose_name="EAN koda skupine izdelkov")

    def __str__(self):
        return self.ime 

class Tag(models.Model):
    ime = models.CharField(max_length = 100, verbose_name="Ime taga")

    def __str__(self):
        return self.ime 

class Izdelek(models.Model):
    ime = models.CharField(max_length=100, verbose_name="Ime izdelka")
    opis = models.TextField(max_length=300, verbose_name="Opis izdelka")
    slika = models.ImageField(upload_to="gallery", verbose_name= "Slika izdelka")
    image_thumbnail = ImageSpecField(source='slika',
                                 
                                 format='JPEG',
                                 options={'quality': 60})
    skupina_izdelkov = models.ForeignKey(SkupinaIzdelkov,  null = True, on_delete=models.SET_NULL)
    tag = models.ManyToManyField(Tag)
    koda = models.CharField(max_length=100, verbose_name="Koda izdelka")

    zaloga = models.BooleanField(default=True, verbose_name="Ali je izdelek na zalogi")
    aktiven = models.BooleanField(default=True, verbose_name="Ali naj bo prikazan na strani")

    def __str__(self):
        return self.ime  



class NarociloIzdelka(models.Model):
    izdelek = models.ForeignKey(Izdelek, null = True, on_delete=models.SET_NULL)
    kolicina = models.IntegerField()


class ProdajnoMesto(models.Model):
   ime = models.CharField(max_length = 100, verbose_name="Ime prodajnega mesta")
   naslov = models.CharField(max_length = 100, verbose_name="Naslov prodajnega mesta")
   postna_stevilka = models.CharField(max_length = 100, verbose_name="Postna številka prodajnega mesta")
   obcina = models.CharField(max_length = 100, verbose_name="Občina prodajnega mesta")
   kontaktna_oseba = models.CharField(max_length = 100, verbose_name="Kontaktna oseba")
   telefon = models.CharField(max_length = 100, verbose_name="Telefonska številka")

class Podjetje(models.Model):
    ime = models.CharField(max_length = 100, verbose_name="Ime podjetja")
    naslov = models.CharField(max_length = 100, verbose_name="Naslov podjetja")
    postna_stevilka = models.CharField(max_length = 100, verbose_name="Poštna številka")
    obcina = models.CharField(max_length = 100, verbose_name="Občina")
    davcna_stevilka = models.CharField(max_length = 100, verbose_name="Davčna številka")

class Uporabnik(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    podjetje = models.ForeignKey(Podjetje, on_delete=models.CASCADE, verbose_name="Podjetje")
    prodajno_mesto = models.ForeignKey(ProdajnoMesto, on_delete=models.CASCADE, verbose_name="Prodajno mesto")

class Narocilo(models.Model):

    uporabnik = models.ForeignKey(Uporabnik, on_delete=models.CASCADE)
    opomba = models.CharField(blank=True, max_length=200)
    # ce ne specificiras datuma se bo shranil trenutni datum
    datum = models.DateTimeField(auto_now_add=True, verbose_name="Datum naročila")
    narocila_izdelka = models.ManyToManyField(NarociloIzdelka)
    

    je_obdelan = models.BooleanField(default=False, verbose_name="Ali je naročilo že obdelano")
    nacin_prodaje = models.CharField(max_length = 100, verbose_name="Način prodaje")
    nacin_dostave = models.CharField(max_length = 100, verbose_name="Način dostave")
    st_narocila = models.CharField(max_length = 100, verbose_name="Številka naročila")

    def __str__(self):
        if self.je_obdelan:
            return "Staro narocilo: " + str(self.id)
        else:
            return "Novo narocilo: " + str(self.id)

#se mi zdi da je vseeno potrebno lociti kosarico od narocil, da ne bo uporabnika kej zmedlo
class Kosarica(models.Model):
    narocila_izdelka = models.ManyToManyField(NarociloIzdelka, blank=True)
    uporabnik = models.ForeignKey(Uporabnik, on_delete=models.CASCADE)
