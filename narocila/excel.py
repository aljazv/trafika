from django.http import HttpResponse, HttpResponseRedirect,JsonResponse , HttpResponseForbidden
from products.models import *
from django.shortcuts import render
import xlwt
from trafika.views import *
from django.db.models import F


from datetime import datetime

import operator

#naredi teste oziromaa matic/verlic preveri delovanje teh funkcij

def prenesi_xls(request):
    if not is_logged_in(request):
      return HttpResponseRedirect("/prijava/")

    if is_normal_user(request):
        return HttpResponseRedirect("/")

    if request.method == 'POST' and 'prenesi_excel_skupine' in request.POST:

        datum_zac = request.POST['datum_zac']
        datum_kon = request.POST['datum_kon']

        datum_split_zac = datum_zac.split("/")
        datum_split_kon = datum_kon.split("/")

        zacetni_datum= datetime(int(datum_split_zac[2]), int(datum_split_zac[1]), int(datum_split_zac[0]))
        koncni_datum = datetime(int(datum_split_kon[2]), int(datum_split_kon[1]), int(datum_split_kon[0]))


        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'inline; filename="poArtiklu.xls"'

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Users')

        # Sheet header, first row
        row_num = 0

        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        columns = ['#', 'EAN koda', 'ime artikla', 'stevilo narocil', ]

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        # Sheet body, remaining rows
        font_style = xlwt.XFStyle()
        

        narocila = Narocilo.objects.filter(datum__range = (zacetni_datum,koncni_datum))
        narocila_izdelka = []
        for narocilo in narocila:
            for narocilo_izdelka in narocilo.narocila_izdelka.all():
                narocila_izdelka.append(narocilo_izdelka)


        #izdelki, kjer EAN koda ni enaka kodi izdelka
        skupineIzdelkov = SkupinaIzdelkov.objects.all()
        tabela = dict((skupina,0) for skupina in skupineIzdelkov)
    
        for narocilo_izdelka in narocila_izdelka:
            if narocilo_izdelka.izdelek.ean_koda != narocilo_izdelka.izdelek.koda:
                tabela[narocilo_izdelka.izdelek.skupina_izdelkov] += narocilo_izdelka.kolicina

        tabela = {x:y for x,y in tabela.items() if y!=0} #izbrises te k so 0!

        tabela_skupine = sorted(tabela.items(), key=operator.itemgetter(1), reverse = True)
        
        for skupina in tabela_skupine:
            row_num += 1
            print(skupina)
            izdelki_za_kodo = Izdelek.objects.filter(skupina_izdelkov = skupina[0])

            ws.write(row_num, 0, str(row_num) + ".", font_style)
            ws.write(row_num, 1, izdelki_za_kodo[0].ean_koda , font_style)
            ws.write(row_num, 2, skupina[0].ime, font_style)
            ws.write(row_num, 3, skupina[1], font_style)

        #Izdelki kjer je EAN koda enaka kodi izdelka
        izdelki = Izdelek.objects.filter(ean_koda = F('koda'))
        tabela_ean = dict((izdelek,0) for izdelek in izdelki)
        for narocilo_izdelka in narocila_izdelka:
            if narocilo_izdelka.izdelek.ean_koda == narocilo_izdelka.izdelek.koda:
                tabela_ean[narocilo_izdelka.izdelek] += narocilo_izdelka.kolicina
        tabela_ean = {x:y for x,y in tabela_ean.items() if y!=0} #izbrises te k so 0!
        tabela_ean_sorted = sorted(tabela_ean.items(), key=operator.itemgetter(1), reverse = True)

        for izdelek in tabela_ean_sorted:
            row_num += 1
            ws.write(row_num, 0, str(row_num) + ".", font_style)
            ws.write(row_num, 1, izdelek[0].ean_koda , font_style)
            ws.write(row_num, 2, izdelek[0].ime, font_style)
            ws.write(row_num, 3, izdelek[1], font_style)

        wb.save(response)
        return response

    if request.method == 'POST' and 'prenesi_excel_skupine_trafika' in request.POST:

        prodajno_mesto_id = request.POST['prodajno_mesto'] # dodatno

        datum_zac = request.POST['datum_zac']
        datum_kon = request.POST['datum_kon']

        datum_split_zac = datum_zac.split("/")
        datum_split_kon = datum_kon.split("/")

        zacetni_datum= datetime(int(datum_split_zac[2]), int(datum_split_zac[1]), int(datum_split_zac[0]))
        koncni_datum = datetime(int(datum_split_kon[2]), int(datum_split_kon[1]), int(datum_split_kon[0]))

        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'inline; filename="PoArtikluInProdajnemMestu.xls"' # se filename spremen

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Users')

        # Sheet header, first row
        row_num = 4

        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        prodajno_mesto = ProdajnoMesto.objects.get(id = prodajno_mesto_id)
        columns = ['Prodajno mesto: ', prodajno_mesto.ime, prodajno_mesto.naslov, prodajno_mesto.obcina, prodajno_mesto.postna_stevilka]
        for col_num in range(len(columns)):
            ws.write(0, col_num, columns[col_num], font_style)

        columns = ['#', 'EAN koda', 'ime artikla', 'stevilo narocil', ]

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        # Sheet body, remaining rows
        font_style = xlwt.XFStyle()
        

        #potrebno preveriti se tole funkcijo
        narocila = Narocilo.objects.filter(datum__range = (zacetni_datum,koncni_datum), uporabnik__prodajno_mesto__id = prodajno_mesto_id) #dodatno prodajno mesto
        narocila_izdelka = []
        for narocilo in narocila:
            for narocilo_izdelka in narocilo.narocila_izdelka.all():
                narocila_izdelka.append(narocilo_izdelka)

        
        #izdelki, kjer EAN koda ni enaka kodi izdelka
        skupineIzdelkov = SkupinaIzdelkov.objects.all()
        tabela = dict((skupina,0) for skupina in skupineIzdelkov)
    
        for narocilo_izdelka in narocila_izdelka:
            if narocilo_izdelka.izdelek.ean_koda != narocilo_izdelka.izdelek.koda:
                tabela[narocilo_izdelka.izdelek.skupina_izdelkov] += narocilo_izdelka.kolicina

        tabela = {x:y for x,y in tabela.items() if y!=0} #izbrises te k so 0!

        tabela_skupine = sorted(tabela.items(), key=operator.itemgetter(1), reverse = True)
        
        count = 0

        for skupina in tabela_skupine:
            row_num += 1
            count += 1
            print(skupina)
            izdelki_za_kodo = Izdelek.objects.filter(skupina_izdelkov = skupina[0])

            ws.write(row_num, 0, str(count) + ".", font_style)
            ws.write(row_num, 1, izdelki_za_kodo[0].ean_koda , font_style)
            ws.write(row_num, 2, skupina[0].ime, font_style)
            ws.write(row_num, 3, skupina[1], font_style)

        #Izdelki kjer je EAN koda enaka kodi izdelka
        izdelki = Izdelek.objects.filter(ean_koda = F('koda'))
        tabela_ean = dict((izdelek,0) for izdelek in izdelki)
        for narocilo_izdelka in narocila_izdelka:
            if narocilo_izdelka.izdelek.ean_koda == narocilo_izdelka.izdelek.koda:
                tabela_ean[narocilo_izdelka.izdelek] += narocilo_izdelka.kolicina
        tabela_ean = {x:y for x,y in tabela_ean.items() if y!=0} #izbrises te k so 0!
        tabela_ean_sorted = sorted(tabela_ean.items(), key=operator.itemgetter(1), reverse = True)

        for izdelek in tabela_ean_sorted:
            row_num += 1
            count += 1
            ws.write(row_num, 0, str(count) + ".", font_style)
            ws.write(row_num, 1, izdelek[0].ean_koda , font_style)
            ws.write(row_num, 2, izdelek[0].ime, font_style)
            ws.write(row_num, 3, izdelek[1], font_style)

        wb.save(response)
        return response

    if request.method == 'POST' and 'prenesi_excel_motivno' in request.POST:
        
        skupina_izdelkov_id = request.POST['skupina_izdelkov']
        datum_zac = request.POST['datum_zac']
        datum_kon = request.POST['datum_kon']

        datum_split_zac = datum_zac.split("/")
        datum_split_kon = datum_kon.split("/")

        zacetni_datum= datetime(int(datum_split_zac[2]), int(datum_split_zac[1]), int(datum_split_zac[0]))
        koncni_datum = datetime(int(datum_split_kon[2]), int(datum_split_kon[1]), int(datum_split_kon[0]))


        print(zacetni_datum)
        print(koncni_datum)
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'inline; filename="motivno.xls"'

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Users')

        # Sheet header, first row
        row_num = 4

        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        skupina_izdelkov = SkupinaIzdelkov.objects.get(id = skupina_izdelkov_id)
        izdelki_za_kodo = Izdelek.objects.filter(skupina_izdelkov = skupina_izdelkov)
        columns = ['Skupina Izdelkov: ', skupina_izdelkov.ime, izdelki_za_kodo[0].ean_koda]
        for col_num in range(len(columns)):
            ws.write(0, col_num, columns[col_num], font_style)


        columns = ['#', 'koda', 'ime artikla', 'stevilo narocil', ]

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        # Sheet body, remaining rows
        font_style = xlwt.XFStyle()
        
        narocila = Narocilo.objects.filter(datum__range = (zacetni_datum,koncni_datum))
        narocila_izdelka = []
        for narocilo in narocila:
            for narocilo_izdelka in narocilo.narocila_izdelka.all():
                narocila_izdelka.append(narocilo_izdelka)

        
        izdelki = Izdelek.objects.filter(skupina_izdelkov__id = skupina_izdelkov_id)
        tabela = dict((izdelek,0) for izdelek in izdelki)
    
        
        for narocilo_izdelka in narocila_izdelka:
            if str(narocilo_izdelka.izdelek.skupina_izdelkov.id) == skupina_izdelkov_id:
                tabela[narocilo_izdelka.izdelek] += narocilo_izdelka.kolicina


        tabela = {x:y for x,y in tabela.items() if y!=0} #izbrises te k so 0!
        
        rows = sorted(tabela.items(), key=operator.itemgetter(1), reverse = True)

        print(rows)
        count = 0
        for row in rows:
            count += 1
            row_num += 1

            ws.write(row_num, 0, str(count) + "." , font_style)
            ws.write(row_num, 1, row[0].koda, font_style)
            ws.write(row_num, 2, row[0].ime, font_style)
            ws.write(row_num, 3, row[1], font_style)


        wb.save(response)
        return response




    if request.method == 'POST' and 'prenesi_excel_motivno_trafika' in request.POST:

        prodajno_mesto_id = request.POST['prodajno_mesto'] # dodatno
        skupina_izdelkov_id = request.POST['skupina_izdelkov']
        datum_zac = request.POST['datum_zac']
        datum_kon = request.POST['datum_kon']

        datum_split_zac = datum_zac.split("/")
        datum_split_kon = datum_kon.split("/")

        zacetni_datum= datetime(int(datum_split_zac[2]), int(datum_split_zac[1]), int(datum_split_zac[0]))
        koncni_datum = datetime(int(datum_split_kon[2]), int(datum_split_kon[1]), int(datum_split_kon[0]))


        print(zacetni_datum)
        print(koncni_datum)
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'inline; filename="poArtikluInProdajnemMestu.xls"'

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Users')

        

        # Sheet header, first row
        row_num = 4

        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        prodajno_mesto = ProdajnoMesto.objects.get(id = prodajno_mesto_id)
        columns = ['Prodajno mesto: ', prodajno_mesto.ime, prodajno_mesto.naslov, prodajno_mesto.obcina, prodajno_mesto.postna_stevilka]
        for col_num in range(len(columns)):
            ws.write(0, col_num, columns[col_num], font_style)

        skupina_izdelkov = SkupinaIzdelkov.objects.get(id = skupina_izdelkov_id)

        izdelki_za_kodo = Izdelek.objects.filter(skupina_izdelkov = skupina_izdelkov)
        columns = ['Skupina Izdelkov: ', skupina_izdelkov.ime, izdelki_za_kodo[0].ean_koda]

        for col_num in range(len(columns)):
            ws.write(1, col_num, columns[col_num], font_style)

        columns = ['#', 'EAN koda', 'ime artikla', 'stevilo narocil']

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        # Sheet body, remaining rows
        font_style = xlwt.XFStyle()
        

        #potrebno preveriti se tole funkcijo
        narocila = Narocilo.objects.filter(datum__range = (zacetni_datum,koncni_datum), uporabnik__prodajno_mesto__id = prodajno_mesto_id)
        narocila_izdelka = []
        for narocilo in narocila:
            #for narocilo_izdelka in narocilo.narocila_izdelka.all():
            for narocilo_izdelka in narocilo.narocila_izdelka.all():
                narocila_izdelka.append(narocilo_izdelka)

        
        #skupineIzdelkov = SkupinaIzdelkov.objects.all()
        #tabela = dict((skupina,0) for skupina in skupineIzdelkov)

        izdelki = Izdelek.objects.filter(skupina_izdelkov__id = skupina_izdelkov_id)
        tabela = dict((izdelek,0) for izdelek in izdelki)
    
        #for narocilo_izdelka in narocila_izdelka:
        #   tabela[narocilo_izdelka.izdelek.skupina_izdelkov] += narocilo_izdelka.kolicina
        
        for narocilo_izdelka in narocila_izdelka:
            if str(narocilo_izdelka.izdelek.skupina_izdelkov.id) == skupina_izdelkov_id:
                tabela[narocilo_izdelka.izdelek] += narocilo_izdelka.kolicina


        tabela = {x:y for x,y in tabela.items() if y!=0} #izbrises te k so 0!
        
        rows = sorted(tabela.items(), key=operator.itemgetter(1), reverse = True)

        print(rows)
        zaporedna_st = 0
        for row in rows:
            zaporedna_st += 1
            row_num += 1
            print(row)
            ws.write(row_num, 0, str(zaporedna_st) + "." , font_style)
            ws.write(row_num, 1, row[0].koda, font_style)
            ws.write(row_num, 2, row[0].ime, font_style)
            ws.write(row_num, 3, row[1], font_style)


        wb.save(response)
        return response



    prodajna_mesta = ProdajnoMesto.objects.all()
    skupine_izdelkov = SkupinaIzdelkov.objects.all()

    context={
        'prodajno_mesto': prodajna_mesta,
        'skupine_izdelkov': skupine_izdelkov
        }



    return render(request,'narocila/statistika.html',context)
