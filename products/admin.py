from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
# Register your models here.
# ENABLES CRUD operations on admin page

from .models import *



class IzdelekAdmin(admin.ModelAdmin):
    list_display = ('ime','ean_koda','koda')
    search_fields = ['id','ean_koda','koda']

class NarociloIzdelkaAdmin(admin.ModelAdmin):
    list_display = ('__str__','id','izdelek')
    search_fields = ['id']

class ProdajnoMestoAdmin(admin.ModelAdmin):
    list_display = ('ime','naslov','potnik')

class PodjetjeAdmin(admin.ModelAdmin):
    list_display = ('ime','naslov')
class UporabnikAdmin(admin.ModelAdmin):
    list_display = ('__str__','podjetje','prodajno_mesto')
class PotnikAdmin(admin.ModelAdmin):
    list_display = ('__str__','telefon','email')

class NarociloAdmin(admin.ModelAdmin):
    list_display = ('__str__','id','datum','st_narocila')
    list_filter = ['datum']
    search_fields = ['id','st_narocila','datum']





admin.site.register(Izdelek,IzdelekAdmin)
admin.site.register(SkupinaIzdelkov)
admin.site.register(Tag)
admin.site.register(Uporabnik,UporabnikAdmin)
admin.site.register(Narocilo,NarociloAdmin)
admin.site.register(NarociloIzdelka,NarociloIzdelkaAdmin)
admin.site.register(Kosarica)
admin.site.register(Potnik,PotnikAdmin)
admin.site.register(ProdajnoMesto,ProdajnoMestoAdmin)
admin.site.register(Podjetje,PodjetjeAdmin)
admin.site.register(PodjetjeGlavno)

UserAdmin.add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'first_name', 'last_name', 'email')}
        ),
    )