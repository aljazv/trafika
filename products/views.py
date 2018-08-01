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

from reportlab.lib import utils

from reportlab.lib import colors
from reportlab.lib.pagesizes import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
pdfmetrics.registerFont(TTFont('GretaSansStd-Bold', 'GretaSansStd-Bold.ttf'))
pdfmetrics.registerFont(TTFont('GretaSansStd-Regular', 'GretaSansStd-Regular.ttf'))
pdfmetrics.registerFont(TTFont('Vera', 'Vera.ttf'))

from reportlab.graphics.shapes import Rect,Drawing

from time import gmtime, strftime
from trafika.views import *

#context: opozorilo je za display informacij

def getAllGroups():
    return SkupinaIzdelkov.objects.all()

#index je glavna stran ki si prikaze ko se uporabnik prijavi
#ce gres na main page te preusmeri na prvo skupino izdelkov
def index(request):

    if not is_logged_in(request):
          return HttpResponseRedirect("/prijava/")

    if is_admin(request):
        return HttpResponseRedirect("/narocila/nova_narocila/")

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
  


#index_skupina je 
# na njej je skupina izdelkov izdelki
def index_skupina(request, index, search_string = None):
    
    #Preveri ce je uporabnik logiran, ce ne gre na login page
    if not is_logged_in(request):
        return HttpResponseRedirect("/prijava/")

    if is_admin(request):
        return HttpResponseRedirect("/")

    #prikaz izdelkov    
    #POSEBNOST - ker ob kreaciji uporabnika se NE naredi kosarica jo moramo cimprej
    #zato je najbolje da se mu naredi kosarica ko se prvic logira na stran, 

    if not Kosarica.objects.filter(uporabnik = Uporabnik.objects.get(user=request.user)).exists():
        nova_kosarica = Kosarica(uporabnik = Uporabnik.objects.get(user=request.user))
        nova_kosarica.save()

    #logika za iskanje po tagih
    if search_string != None:
        vsi_izdelki = Izdelek.objects.filter(tag__ime__istartswith=search_string).filter(skupina_izdelkov__id = index).filter(aktiven=True).order_by('ime')
        
        #ce ne najde nobenega izdelka poskusi se z kodo izdelka
        if not vsi_izdelki.exists():
            vsi_izdelki = Izdelek.objects.filter(koda__istartswith=search_string).filter(skupina_izdelkov__id = index).filter(aktiven=True).order_by('ime')
    else:
        vsi_izdelki = Izdelek.objects.filter(aktiven=True).filter(skupina_izdelkov__id = index).order_by('ime')
    

    skupina = SkupinaIzdelkov.objects.get(id=index);

    #paginacija
    paginator = Paginator(vsi_izdelki, 7)
    page = request.GET.get('page')
    paginirani_izdelki = paginator.get_page(page)

    context = {
        'opozorilo' : vsi_izdelki.count() == 0,
        'skupine': getAllGroups(),
        'izdelki' : paginirani_izdelki,
        'index_skupina' : index,
        'search_string': search_string,
        'skupina': skupina
        
    }

    return render(request,'products/index.html',context)

# vrne izdelke ki se ujemajo v tagu s search_stringom
def search(request, index , search_string):
    
    
    return index_skupina(request,index,search_string=search_string)

def kosarica(request):

    #Preveri ce je uporabnik logiran, ce ne gre na login page
    if not is_logged_in(request):
          return HttpResponseRedirect("/prijava/")

    if is_admin(request):
        return HttpResponseRedirect("/")

    #dela ker je sam ena kosrica ustvarjena!
    #Za popraviti sumnike
    #plus se dimenzije slik
    if request.method == 'POST' and 'odstrani_izdelek' in request.POST:

        narocilo_izdelka_id = request.POST['narocilo']
        narocilo_izdelka = NarociloIzdelka.objects.filter(id = narocilo_izdelka_id)
        narocilo_izdelka.delete()

    elif request.method == 'POST':
        print("KLKl")
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

    if not is_logged_in(request):
        return HttpResponseRedirect("/prijava/")

    if is_admin(request):
        return HttpResponseRedirect("/")

    set_msg = False
    if request.method == 'POST' and 'oddaj_narocilo' in request.POST:
        curr_opomba = request.POST['opomba']

        set_msg = True
        kosarica_uporabnika = Kosarica.objects.get(uporabnik__user = request.user)
        curr_uporabnik = Uporabnik.objects.get(user = request.user)

        potnik = Potnik.objects.get(prodajno_mesto = curr_uporabnik.prodajno_mesto) #dodas se potnika!
        narocilo = Narocilo(uporabnik = curr_uporabnik, opomba = curr_opomba, potnik = potnik)
        narocilo.save()
        for narocilo_add in kosarica_uporabnika.narocila_izdelka.all():
            narocilo.narocila_izdelka.add(narocilo_add)
            narocilo.save()

        kosarica_uporabnika.narocila_izdelka.clear()
        return HttpResponseRedirect('/pregled_narocil/') #da ne submita forme se enkrat

    if request.method == 'POST' and 'prenesi_pdf' in request.POST:
        narocilo_id = request.POST['narocilo_id']
        narocilo = Narocilo.objects.get(id = narocilo_id)
        

        leto_dobavnice = narocilo.datum.strftime("%Y")
        st_dobavnice = leto_dobavnice[-2:] + str(narocilo.id).zfill(4)
        ime_datoteke = "narocilnica" + "_" + st_dobavnice + ".pdf"
        story=[]
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="{}"'.format(ime_datoteke)
        doc = SimpleDocTemplate(response,pagesize=letter,
            rightMargin=20,leftMargin=20,
            topMargin=20,bottomMargin=20)

        story = natisni_narocilnica(request,narocilo)
        doc.build(story)
        return response

    curr_uporabnik = Uporabnik.objects.get(user = request.user)
    narocila_uporabnika = Narocilo.objects.filter(uporabnik = curr_uporabnik)
    
    #tle skos vrze narocilo uspesno dodano -- > loh se tut zbrise. Simple.

    context = {
        'arr': narocila_uporabnika,
        'msg_type': 'alert-success',
        'message': 'Naročilo uspešno oddano.',
        'show_msg': set_msg,
        'skupine': getAllGroups(),
        }

    return render(request,'products/pregled_narocil.html',context)

def natisni_narocilnica(request, narocilo):
    

    narocila_izdelka = narocilo.narocila_izdelka.all()
        
    uporabnik = narocilo.uporabnik
    story = []

    formatted_time = datetime.date.today()
    formatted_time = str(formatted_time)
    tabela = formatted_time.split("-")
    formatted_time = tabela[2] + "." + tabela[1] + "." + tabela[0]

    #GretaSansStd-Bold
    #GretaSansStd-Regular
            
    styles=getSampleStyleSheet()
    p0 = ParagraphStyle('MyNormal',parent=styles['Normal'], alignment=TA_RIGHT)
    p1 = styles.add(ParagraphStyle(name='Center',fontName='GretaSansStd-Regular', alignment=TA_CENTER))
    p2 = styles.add(ParagraphStyle(name='Right',fontName='GretaSansStd-Regular', alignment=TA_RIGHT))
    p3 = styles.add(ParagraphStyle(name='Left',fontName='GretaSansStd-Regular', alignment=TA_LEFT))
    p4 = styles.add(ParagraphStyle(name='Line_Data',fontName='GretaSansStd-Regular', alignment=TA_LEFT, fontSize=9, leading=14))
    p5 = styles.add(ParagraphStyle(name='Line_Data_Small',fontName='GretaSansStd-Regular', alignment=TA_LEFT, fontSize=7, leading=14))
    p6 = styles.add(ParagraphStyle(name='Line_Data_Large',fontName='GretaSansStd-Regular', alignment=TA_LEFT, fontSize=10, leading=14))
    p7 = styles.add(ParagraphStyle(name='Line_Data_Largest',fontName='GretaSansStd-Regular', alignment=TA_LEFT, fontSize=20, leading=14))
    p8 = styles.add(ParagraphStyle(name='Line_Label',fontName='GretaSansStd-Bold', font='GretaSansStd-Bold', fontSize=8, leading=14, alignment=TA_LEFT))
    p9 = styles.add(ParagraphStyle(name='Line_Label_Center',fontName='GretaSansStd-Bold', font='GretaSansStd-Bold', fontSize=14, alignment=TA_CENTER))
    
    styles.add(ParagraphStyle(name='sidarta_label',fontName='GretaSansStd-Bold', font='GretaSansStd-Bold', fontSize=17, leading=14, alignment=TA_LEFT))
    
    width=6*cm
    logo_path = "media/gallery/logo.jpg"
    img = utils.ImageReader(logo_path)
    iw, ih = img.getSize()
    aspect = ih / float(iw)
    logo_slika = Image(logo_path, width=width, height=(width * aspect))

    data1 = [[Paragraph('NAROČILNICA', styles["Line_Data_Largest"]),
            Paragraph('', styles["Line_Label"]),
            logo_slika
            ]]
        
    t1 = Table(data1, colWidths=(10* cm,1.9 * cm,8 * cm), rowHeights = (0.5*cm))
    t1.setStyle(TableStyle([
        #('BACKGROUND',(2,0),(2,0),colors.black)
        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
    ]))
    story.append(t1)

    story.append(Spacer(1, 30))

    #
    podjetje = uporabnik.podjetje
    prodajno_mesto = uporabnik.prodajno_mesto

    podjetje_podatki = '%s <br/> %s <br/> %s, %s <br/> %s <br/> ' % (podjetje.ime, podjetje.naslov, podjetje.postna_stevilka, podjetje.obcina, podjetje.davcna_stevilka)
        
    prodajno_mesto_podatki = '%s <br/>%s <br/>%s %s <br/>' % (prodajno_mesto.ime, prodajno_mesto.naslov, prodajno_mesto.postna_stevilka, prodajno_mesto.obcina)

    sidarta = 'Trpinčeva 41c, SI - 1000 Ljubljana <br/>tel • 01 561 34 73, fax • 0590 72897 <br/>office@sidarta.si <br/> www.sidarta.si'


    prodajno_mesto.kontaktna_oseba,prodajno_mesto.telefon
    leto_dobavnice = narocilo.datum.strftime("%Y")
    st_dobavnice = leto_dobavnice[-2:] + str(narocilo.id).zfill(4)

    datum = narocilo.datum.strftime("%d.%m.%Y, %H:%M")

    data1 = [#1 vrstica
             [Paragraph('Prodajno mesto/naslov dostave', styles["Line_Label"]),
              Paragraph('Številka naročilnice', styles["Line_Label"]),
              Paragraph('', styles["sidarta_label"])
              ],
              #2
             [Paragraph(prodajno_mesto_podatki, styles["Line_Data_Large"]),
              Paragraph(st_dobavnice, styles["Line_Data_Large"]),
              Paragraph(sidarta, styles["Line_Data_Small"])
              ],
              #3
              [Paragraph('', styles["Line_Label"]),
              Paragraph('Datum naročila', styles["Line_Label"]),
              Paragraph('', styles["Line_Label"])
              ],
              #4
              [Paragraph('', styles["Line_Data_Large"]),
              Paragraph(datum, styles["Line_Data_Large"]),
              Paragraph('', styles["Line_Data_Large"])
              ],
              #5
              [Paragraph('Kontaktna oseba', styles["Line_Label"]),
              Paragraph('', styles["Line_Label"]),
              Paragraph('Potnik', styles["Line_Label"])
              ],
              #6
              [Paragraph(prodajno_mesto.kontaktna_oseba, styles["Line_Data_Large"]),
              Paragraph('', styles["Line_Data_Large"]),
              Paragraph(narocilo.potnik.user.first_name + " " + narocilo.potnik.user.last_name, styles["Line_Data_Large"])
              ],
              #7
              [Paragraph('Telefon', styles["Line_Label"]),
              Paragraph('', styles["Line_Label"]),
              Paragraph('Telefon', styles["Line_Label"])
              ],
              #8
              [Paragraph(prodajno_mesto.telefon, styles["Line_Data_Large"]),
              Paragraph('', styles["Line_Data_Large"]),
              Paragraph(narocilo.potnik.telefon, styles["Line_Data_Large"])
              ],
              #9
              [Paragraph('Sedež podjetja', styles["Line_Label"]),
              Paragraph('', styles["Line_Label"]),
              Paragraph('mail', styles["Line_Label"])
              ],
              #10
              [Paragraph(podjetje_podatki, styles["Line_Data"]),
              Paragraph('', styles["Line_Data_Large"]),
              Paragraph(narocilo.potnik.email, styles["Line_Data_Large"])
              ],
              #11
              [Paragraph('', styles["Line_Label"]),
              Paragraph('', styles["Line_Label"]),
              Paragraph('', styles["Line_Label"])
              ],
              #12
              [Paragraph('', styles["Line_Data_Large"]),
              Paragraph('', styles["Line_Data_Large"]),
              Paragraph('', styles["Line_Data_Large"])
              ]
              ]

    t1 = Table(data1, colWidths=(6.6 * cm), rowHeights = (0.5*cm, 1*cm,0.5*cm, 1*cm,0.5*cm, 1*cm,0.5*cm, 1*cm,0.5*cm, 1*cm,0.5*cm, 1*cm,), hAlign='LEFT')

    t1.setStyle(TableStyle([
        ('VALIGN',(0,0),(-1,-1),'TOP'),
        ('VALIGN',(2,1),(2,1),'MIDDLE'),
        ('SPAN',(0,1),(0,3)),
        ('SPAN',(2,1),(2,3)),
        ('SPAN',(0,9),(0,11)),
        ('LINEBELOW', (2, 3), (2, 3), 2, colors.black)
    ]))
    story.append(t1)
    #
    story.append(Spacer(1, 12))
    #
    ptext = 'Opombe: %s' % narocilo.opomba
    par = Paragraph(ptext, styles["Line_Data"])
    story.append(par)
    #
    story.append(Spacer(1, 12))
    #
    data1 = [[Paragraph('#', styles["Line_Label"]),
        Paragraph('IME IZDELKA', styles["Line_Label"]),
        Paragraph('SLIKA', styles["Line_Label"]),
        Paragraph('KODA IZDELKA', styles["Line_Label"]),
        Paragraph('VRSTA IZDELKA', styles["Line_Label"]),
        Paragraph('KOLIČINA', styles["Line_Label"]),
        Paragraph('', styles["Line_Label"])
        ]]
        
    t1 = Table(data1, colWidths=(1 * cm, 3.6 * cm,4.75 * cm, 5 * cm, 3 * cm, 1.6 * cm, 0.8 * cm))
    t1.setStyle(TableStyle([
        ('LINEBELOW', (0, 0), (-1, -1), 0.25, colors.black)
    ]))
    story.append(t1)
    #
    d = Drawing(15, 15)
    d.add(Rect(0, 0, 15, 15,strokeColor=colors.black,fillColor=colors.white, strokeWidth=1))
    
    for i, narocilo_izdelka in enumerate(narocila_izdelka):
        iteracija = str(i+1) + "."
        img = utils.ImageReader(narocilo_izdelka.izdelek.image_thumbnail)
        iw, ih = img.getSize()
        aspect = ih / float(iw)

        im = Image(narocilo_izdelka.izdelek.image_thumbnail, 2*cm, 2*cm*aspect)

        data1 = [[Paragraph(iteracija, styles["Line_Data"]),
                Paragraph(narocilo_izdelka.izdelek.ime, styles["Line_Data"]),
                im,
                Paragraph(narocilo_izdelka.izdelek.koda, styles["Line_Data"]),
                Paragraph(narocilo_izdelka.izdelek.skupina_izdelkov.ime, styles["Line_Data"]),
                Paragraph(str(narocilo_izdelka.kolicina), styles["Line_Data"]),
                d
                ]]

        t1 = Table(data1, colWidths=(1 * cm, 3.6 * cm, 4.75 * cm, 5 * cm, 3 * cm, 1.6 * cm, 0.8 * cm))
        t1.setStyle(TableStyle([
            ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
            ('LINEBELOW', (0, 0), (-1, -1), 0.25, colors.black)
        ]))
        story.append(t1)

    return story
