from django.contrib import admin

# Register your models here.
# ENABLES CRUD operations on admin page

from .models import *

admin.site.register(Izdelek)
admin.site.register(SkupinaIzdelkov)
admin.site.register(Tag)
admin.site.register(Uporabnik)
admin.site.register(Narocilo)
admin.site.register(NarociloIzdelka)
admin.site.register(Kosarica)

