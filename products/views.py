from django.http import HttpResponse, HttpResponseRedirect,JsonResponse , HttpResponseForbidden
from django.core.paginator import Paginator
from django.template import loader
from django.shortcuts import render
import datetime

from .models import *
from .forms import *

import os.path

from reportlab.lib.enums import TA_JUSTIFY, TA_RIGHT, TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics

from reportlab.lib import colors
from reportlab.lib.pagesizes import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak

from time import gmtime, strftime


#context: opozorilo je za display informacij

def getAllGroups():
    return SkupinaIzdelkov.objects.all()

#index je glavna stran ki si prikaze ko se uporabnik prijavi
#ce gres na main page te preusmeri na prvo skupino izdelkov
def index(request):

    if request.user.is_authenticated:

            #dodajanje izdelkov v koscarico preko AJAX
        if request.method == 'POST':
            #print(request.user)
            #print(request.POST)
            #print(request.POST['kolicina'])
        
            uporabnik = Uporabnik.objects.get(user=request.user)
            kosarica_uporabnika = Kosarica.objects.get(uporabnik=uporabnik)

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
            prva_skupina = SkupinaIzdelkov.objects.first().id
            return HttpResponseRedirect(str(prva_skupina)+ "/")
    else:
        return HttpResponseRedirect("/prijava/")


#index_skupina je 
# na njej je skupina izdelkov izdelki
def index_skupina(request, index, search_string = None):
    
    #Preveri ce je uporabnik logiran, ce ne gre na login page
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/prijava/")

    #prikaz izdelkov    
    else:

        #POSEBNOST - ker ob kreaciji uporabnika se NE naredi kosarica jo moramo cimprej
        #zato je najbolje da se mu naredi kosarica ko se prvic logira na stran, 

        if not Kosarica.objects.filter(uporabnik = Uporabnik.objects.get(user=request.user)).exists():
            nova_kosarica = Kosarica(uporabnik = Uporabnik.objects.get(user=request.user))
            nova_kosarica.save()
            print("kosarica ustvarjena")



        #logika za iskanje po tagih
        if search_string != None:
            vsi_izdelki = Izdelek.objects.filter(tag__ime__istartswith=search_string).filter(skupina_izdelkov__id = index).filter(aktiven=True).order_by('ime')
            
        else:
            vsi_izdelki = Izdelek.objects.filter(aktiven=True).filter(skupina_izdelkov__id = index).order_by('ime')
        


        #paginacija
        paginator = Paginator(vsi_izdelki, 25)
        page = request.GET.get('page')
        paginirani_izdelki = paginator.get_page(page)



        context = {
            'opozorilo' : 'nic',
            'skupine': getAllGroups(),
            'izdelki' : paginirani_izdelki,
            'index_skupina' : index,
            
        }

        return render(request,'products/index.html',context)

# vrne izdelke ki se ujemajo v tagu s search_stringom
def search(request, index , search_string):
    
    
    return index_skupina(request,index,search_string=search_string)

def kosarica(request):

    #Preveri ce je uporabnik logiran, ce ne gre na login page
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/prijava/")

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

    kosarica_uporabnika = Kosarica.objects.get(uporabnik__user = request.user)
    narocila_izdelkov = kosarica_uporabnika.narocila_izdelka.all()
    
    context = {
        'arr': narocila_izdelkov,
        'skupine': getAllGroups(),
        }

    return render(request,'products/kosarica.html',context)

def pregled_narocil(request):

    #Preveri ce je uporabnik logiran, ce ne gre na login page
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/prijava")

    if request.method == 'POST' and 'oddaj_narocilo' in request.POST:
        curr_opomba = request.POST['opomba']

        kosarica_uporabnika = Kosarica.objects.get(uporabnik__user = request.user)
        curr_uporabnik = Uporabnik.objects.get(user = request.user)

        narocilo = Narocilo(uporabnik = curr_uporabnik, opomba = curr_opomba)
        narocilo.save()
        for narocilo_add in kosarica_uporabnika.narocila_izdelka.all():
            narocilo.narocila_izdelka.add(narocilo_add)
            narocilo.save()

        kosarica_uporabnika.narocila_izdelka.clear()
        return HttpResponseRedirect('/pregled_narocil/') #da ne submita forme se enkrat

    if request.method == 'POST' and 'prenesi_pdf' in request.POST:

        narocilo_id = request.POST['narocilo_id']
        narocilo = Narocilo.objects.get(id = narocilo_id)

        narocila_izdelka = narocilo.narocila_izdelka.all()
        
        uporabnik = Uporabnik.objects.get(user = request.user)

        story=[]
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="narocilo.pdf"'
        doc = SimpleDocTemplate(response,pagesize=letter,
                rightMargin=20,leftMargin=20,
                topMargin=20,bottomMargin=20)

        formatted_time = datetime.date.today()
        formatted_time = str(formatted_time)
        tabela = formatted_time.split("-")
        formatted_time = tabela[2] + "." + tabela[1] + "." + tabela[0]

            
        styles=getSampleStyleSheet()
        p0 = ParagraphStyle('MyNormal',parent=styles['Normal'], alignment=TA_RIGHT)
        p1 = styles.add(ParagraphStyle(name='Center', alignment=TA_CENTER))
        p2 = styles.add(ParagraphStyle(name='Right', alignment=TA_RIGHT))
        p3 = styles.add(ParagraphStyle(name='Left', alignment=TA_LEFT))
        p4 = styles.add(ParagraphStyle(name='Line_Data', alignment=TA_LEFT, fontSize=11, leading=10))
        p5 = styles.add(ParagraphStyle(name='Line_Data_Small', alignment=TA_LEFT, fontSize=7, leading=8))
        p6 = styles.add(ParagraphStyle(name='Line_Data_Large', alignment=TA_LEFT, fontSize=12, leading=12))
        p7 = styles.add(ParagraphStyle(name='Line_Data_Largest', alignment=TA_LEFT, fontSize=14, leading=15))
        p8 = styles.add(ParagraphStyle(name='Line_Label', font='Helvetica-Bold', fontSize=7, leading=6, alignment=TA_LEFT))
        p9 = styles.add(ParagraphStyle(name='Line_Label_Center', font='Helvetica-Bold', fontSize=7, alignment=TA_CENTER))

        ptext = '<font size=12>%s</font>' % formatted_time
        par = Paragraph(ptext, p0)
        story.append(par)
        story.append(Spacer(1, 12))
 
        # prodajno mesto + podjetje
        podjetje = uporabnik.podjetje
        prodajno_mesto = uporabnik.prodajno_mesto

        podjetje_podatki = '%s <br/> %s <br/> %s, %s <br/> %s <br/> ' % (podjetje.podjetje, podjetje.naslov, podjetje.postna_stevilka, podjetje.obcina, podjetje.davcna_stevilka)
        
        prodajno_mesto_podatki = '%s <br/>%s <br/>%s, %s <br/>%s <br/>%s <br/>' % (prodajno_mesto.ime, prodajno_mesto.naslov, prodajno_mesto.postna_stevilka, prodajno_mesto.obcina, prodajno_mesto.kontaktna_oseba,prodajno_mesto.telefon)


        data1 = [[Paragraph('Prodajno mesto', styles["Line_Label"]),
                  Paragraph('Podjetje', styles["Line_Label"])],

                 [Paragraph(prodajno_mesto_podatki, styles["Line_Data_Large"]),
                  Paragraph(podjetje_podatki, styles["Line_Data_Large"])]
                 ]

        t1 = Table(data1)
        t1.setStyle(TableStyle([
            ('INNERGRID', (0, 0), (1, 0), 0.25, colors.black),
            ('INNERGRID', (0, 1), (1, 1), 0.25, colors.black),
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        story.append(t1)
        #
        story.append(Paragraph("NAROČILO", styles["Line_Label_Center"]))
        #
        datum = narocilo.datum.strftime("%d.%m.%Y, %H:%M")
        
        data1 = [[Paragraph('DATUM NAROČILA', styles["Line_Label"])],
                [Paragraph(datum, styles["Line_Data_Largest"])
             ]]
        t1 = Table(data1)
        t1.setStyle(TableStyle([
            ('INNERGRID', (0, 0), (1, 0), 0.25, colors.black),
            ('INNERGRID', (0, 1), (1, 1), 0.25, colors.black),
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        story.append(t1)
        #
        data1 = [[Paragraph('#', styles["Line_Label"]),
            Paragraph('IME IZDELKA', styles["Line_Label"]),
            Paragraph('SLIKA', styles["Line_Label"]),
            Paragraph('KODA IZDELKA', styles["Line_Label"]),
            Paragraph('VRSTA IZDELKA', styles["Line_Label"]),
            Paragraph('KOLIČINA', styles["Line_Label"]),
            Paragraph('✔', styles["Line_Label"])
            ]]
        
        t1 = Table(data1, colWidths=(1 * cm, 3.6 * cm,5 * cm, 5 * cm, 3 * cm, 1.6 * cm, 0.8 * cm))
        t1.setStyle(TableStyle([
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        story.append(t1)
        #

        for i, narocilo_izdelka in enumerate(narocila_izdelka):
            iteracija = str(i+1) + "."
            #fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), narocilo_izdelka.izdelek.image_thumbnail.url)
            #im = Image(narocilo_izdelka.izdelek.image_thumbnail.url, 2*cm, 2*cm)

            data1 = [[Paragraph(iteracija, styles["Line_Data"]),
                  Paragraph(narocilo_izdelka.izdelek.ime, styles["Line_Data"]),
                  Paragraph( "Vnesi sliko - fix", styles["Line_Data"]),
                  Paragraph(narocilo_izdelka.izdelek.koda, styles["Line_Data"]),
                  Paragraph(narocilo_izdelka.izdelek.skupina_izdelkov.ime, styles["Line_Data"]),
                  Paragraph(str(narocilo_izdelka.kolicina), styles["Line_Data"]),
                  Paragraph("", styles["Line_Data"])
                  ]]

            t1 = Table(data1, colWidths=(1 * cm, 3.6 * cm, 5 * cm, 5 * cm, 3 * cm, 1.6 * cm, 0.8 * cm))
            t1.setStyle(TableStyle([
                ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ]))
            story.append(t1)



        doc.build(story)

        return response

    curr_uporabnik = Uporabnik.objects.get(user = request.user)
    narocila_uporabnika = Narocilo.objects.filter(uporabnik = curr_uporabnik)
    
    #tle skos vrze narocilo uspesno dodano -- > loh se tut zbrise. Simple.

    context = {
        'arr': narocila_uporabnika,
        'msg_type': 'alert-success',
        'message': 'Naročilo uspešno oddano.',
        'skupine': getAllGroups(),
        }

    return render(request,'products/pregled_narocil.html',context)