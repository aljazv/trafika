from django.http import HttpResponse, HttpResponseRedirect,JsonResponse , HttpResponseForbidden
from django.core.paginator import Paginator
from django.template import loader
from django.shortcuts import render
import datetime

from products.views import *
from . import excel

from products.models import *


# Create your views here.


def nova_narocila(request):

    if request.user.is_authenticated:
        if request.method == 'POST' and 'obdelano' in request.POST:
            narocilo_id = request.POST['narocilo_id']
            narocilo = Narocilo.objects.get(id = narocilo_id)
            narocilo.je_obdelan = True
            narocilo.save()
        if request.method == 'POST' and 'prenesi' in request.POST:
          
            narocilo_id = request.POST['narocilo_id']
            narocilo = Narocilo.objects.get(id = narocilo_id)
            ime_datoteke = "narocilnica" + str(narocilo.id) + ".pdf"
            story=[]
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'inline; filename="{}"'.format(ime_datoteke)
            doc = SimpleDocTemplate(response,pagesize=letter,
              rightMargin=20,leftMargin=20,
              topMargin=20,bottomMargin=20)

            story = natisni_narocilnica(request,narocilo)
            doc.build(story)
            return response


        narocila_neobdelano = Narocilo.objects.filter(je_obdelan = False)

        context = {
          'narocila_neobdelano': narocila_neobdelano
          }

        return render(request,'narocila/nova_narocila.html',context)
    else:
        return HttpResponseRedirect("/prijava/")

def stara_narocila(request):

    if request.user.is_authenticated:
        if request.method == 'POST' and 'uveljavi' in request.POST:
            narocilo_id = request.POST['narocilo_id']
            nacin_prodaje = request.POST['nacinProdaje']
            nacin_dostave = request.POST['nacinDostave']
            narocilo = Narocilo.objects.get(id = narocilo_id)
            narocilo.nacin_prodaje = nacin_prodaje
            narocilo.nacin_dostave = nacin_dostave
            narocilo.save()

        if request.method == 'POST' and 'prenesi_narocilnica' in request.POST:
            narocilo_id = request.POST['narocilo_id']
            narocilo = Narocilo.objects.get(id = narocilo_id)
            ime_datoteke = "narocilnica" + str(narocilo.id) + ".pdf"
            story=[]
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'inline; filename="{}"'.format(ime_datoteke)
            doc = SimpleDocTemplate(response,pagesize=letter,
                rightMargin=20,leftMargin=20,
                topMargin=20,bottomMargin=20)

            story = natisni_narocilnica(request,narocilo)
            doc.build(story)
            return response

        if request.method == 'POST' and 'prenesi_dobavnica' in request.POST:

            # dobavnica ID!
            

            narocilo_id = request.POST['narocilo_id']
            narocilo = Narocilo.objects.get(id = narocilo_id)
            ime_datoteke = "dobavnica" + str(narocilo.id) + ".pdf"
            story=[]
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'inline; filename="{}"'.format(ime_datoteke)
            doc = SimpleDocTemplate(response,pagesize=letter,
                rightMargin=20,leftMargin=20,
                topMargin=20,bottomMargin=20)

            story = natisni_dobavnica(request,narocilo)
            doc.build(story)
            return response
        if request.method == 'POST' and 'uveljavi_stNarocila' in request.POST:
            narocilo_id = request.POST['narocilo_id']
            st_narocila = request.POST['st_narocila']
            narocilo = Narocilo.objects.get(id = narocilo_id)
            narocilo.st_narocila = st_narocila
            narocilo.save()


        narocila_obdelano = Narocilo.objects.filter(je_obdelan = True)

        context = {
            'narocila_obdelano': narocila_obdelano
            }

        return render(request,'narocila/stara_narocila.html',context)

    else:
        return HttpResponseRedirect("/prijava/")


def natisni_dobavnica(request, narocilo):
    narocila_izdelka = narocilo.narocila_izdelka.all()
    #prestejes za skupino izdelkov!!
    #list vseh imen skupine izdelkov + filas, ce je nakonc ksn nic ga ne das na dobavnico. Hash table,dictionary
    skupineIzdelkov = SkupinaIzdelkov.objects.all()
    
    tabela = dict((skupina,0) for skupina in skupineIzdelkov)
    
    for narocilo_izdelka in narocila_izdelka:
        tabela[narocilo_izdelka.izdelek.skupina_izdelkov] += narocilo_izdelka.kolicina

    tabela = {x:y for x,y in tabela.items() if y!=0} #izbrises te k so 0!

    uporabnik = narocilo.uporabnik
    story = []

    formatted_time = datetime.date.today()
    formatted_time = str(formatted_time)
    tabela1 = formatted_time.split("-")
    formatted_time = tabela1[2] + "." + tabela1[1] + "." + tabela1[0]

            
    styles=getSampleStyleSheet()
    p0 = ParagraphStyle('MyNormal',parent=styles['Normal'], alignment=TA_RIGHT)
    p1 = styles.add(ParagraphStyle(name='Center',fontName='Vera', alignment=TA_CENTER))
    p2 = styles.add(ParagraphStyle(name='Right',fontName='Vera', alignment=TA_RIGHT))
    p3 = styles.add(ParagraphStyle(name='Left',fontName='Vera', alignment=TA_LEFT))
    p4 = styles.add(ParagraphStyle(name='Line_Data',fontName='Vera', alignment=TA_LEFT, fontSize=9, leading=13))
    p5 = styles.add(ParagraphStyle(name='Line_Data_Small',fontName='Vera', alignment=TA_LEFT, fontSize=7, leading=8))
    p6 = styles.add(ParagraphStyle(name='Line_Data_Large',fontName='Vera', alignment=TA_LEFT, fontSize=12, leading=13))
    p7 = styles.add(ParagraphStyle(name='Line_Data_Largest',fontName='Vera', alignment=TA_LEFT, fontSize=14, leading=15))
    p8 = styles.add(ParagraphStyle(name='Line_Label',fontName='Vera', font='Helvetica-Bold', fontSize=7, leading=6, alignment=TA_LEFT))
    p9 = styles.add(ParagraphStyle(name='Line_Label_Center',fontName='Vera', font='Helvetica-Bold', fontSize=7, alignment=TA_CENTER))
    
    styles.add(ParagraphStyle(name='sidarta_label',fontName='Vera', font='Helvetica-Bold', fontSize=15, leading=6, alignment=TA_LEFT))
    #ptext = '<font size=12>%s</font>' % formatted_time #čas ko se natisne
    #par = Paragraph(ptext, p0)
    #story.append(par)
    
    #ptext = '<font size=20>DOBAVNICA</font>'
    #par = Paragraph(ptext, styles["Line_Data_Largest"])
    #story.append(par)

    data1 = [[Paragraph('DOBAVNICA', styles["Line_Data_Largest"]),
            Paragraph('', styles["Line_Label"]),
            Paragraph('', styles["Line_Label"])
            ]]
        
    t1 = Table(data1, colWidths=(6.6 * cm,6.6 * cm,6.6 * cm), rowHeights = (0.5*cm))
    t1.setStyle(TableStyle([
        ('BACKGROUND',(2,0),(2,0),colors.black)
    ]))
    story.append(t1)

    story.append(Spacer(1, 30))


 
    # prodajno mesto + podjetje
    podjetje = uporabnik.podjetje
    prodajno_mesto = uporabnik.prodajno_mesto

    podjetje_podatki = '%s <br/> %s <br/> %s, %s <br/> %s <br/> ' % (podjetje.ime, podjetje.naslov, podjetje.postna_stevilka, podjetje.obcina, podjetje.davcna_stevilka)
        
    prodajno_mesto_podatki = '%s <br/>%s <br/>%s %s <br/>' % (prodajno_mesto.ime, prodajno_mesto.naslov, prodajno_mesto.postna_stevilka, prodajno_mesto.obcina)

    sidarta = 'Trpinčeva 41c, SI - 1000 Ljubljana <br/>tel • 01 561 34 73, fax • 0590 72897 <br/>office@sidarta.si <br/> www.sidarta.si'

    print(prodajno_mesto_podatki)

    prodajno_mesto.kontaktna_oseba,prodajno_mesto.telefon
    leto_dobavnice = narocilo.datum.strftime("%Y")
    st_dobavnice = leto_dobavnice[-2:] + str(narocilo.id).zfill(4)

    datum = narocilo.datum.strftime("%d.%m.%Y, %H:%M")

    data1 = [#1 vrstica
             [Paragraph('Prodajno mesto/naslov dostave', styles["Line_Label"]),
              Paragraph('Številka dobavnice', styles["Line_Label"]),
              Paragraph('SIDARTA', styles["sidarta_label"])
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
              Paragraph('Način prodaje', styles["Line_Label"]),
              Paragraph('Potnik', styles["Line_Label"])
              ],
              #6
              [Paragraph(prodajno_mesto.kontaktna_oseba, styles["Line_Data_Large"]),
              Paragraph(narocilo.nacin_prodaje, styles["Line_Data_Large"]),
              Paragraph(narocilo.potnik.user.first_name + " " + narocilo.potnik.user.last_name, styles["Line_Data_Large"])
              ],
              #7
              [Paragraph('Telefon', styles["Line_Label"]),
              Paragraph('Način Dostave', styles["Line_Label"]),
              Paragraph('Telefon', styles["Line_Label"])
              ],
              #8
              [Paragraph(prodajno_mesto.telefon, styles["Line_Data_Large"]),
              Paragraph(narocilo.nacin_dostave, styles["Line_Data_Large"]),
              Paragraph(narocilo.potnik.telefon, styles["Line_Data_Large"])
              ],
              #9
              [Paragraph('Sedež podjetja', styles["Line_Label"]),
              Paragraph('', styles["Line_Label"]),
              Paragraph('mail', styles["Line_Label"])
              ],
              #10
              [Paragraph(podjetje_podatki, styles["Line_Data_Large"]),
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

    t1 = Table(data1, colWidths=(6.6 * cm), rowHeights = (0.5*cm, 1.4*cm,0.5*cm, 1*cm,0.5*cm, 1*cm,0.5*cm, 1*cm,0.5*cm, 1*cm,0.5*cm, 1*cm,), hAlign='LEFT')

    t1.setStyle(TableStyle([
        ('VALIGN',(0,0),(-1,-1),'TOP'),
        ('VALIGN',(2,1),(2,1),'MIDDLE'), # naslov sidarte na sredini
        #('BOX', (0, 0), (-1, -1), 0.25, colors.black),
        ('SPAN',(0,1),(0,3)),
        ('SPAN',(2,1),(2,3)),
        ('SPAN',(0,9),(0,11)),
        ('LINEBELOW', (2, 3), (2, 3), 2, colors.black)
    ]))
    story.append(t1)

    #
    story.append(Spacer(1, 20))
    
    #
    data1 = [[Paragraph('št', styles["Line_Label"]),
            Paragraph('črtna koda EAN', styles["Line_Label"]),
            Paragraph('artikel', styles["Line_Label"]),
            Paragraph('šifra', styles["Line_Label"]),
            Paragraph('količina', styles["Line_Label"])
            ]]
        
    t1 = Table(data1, colWidths=(1 * cm, 6 * cm,5 * cm,2.7*cm, 5 * cm))
    t1.setStyle(TableStyle([
        ('LINEBELOW', (0, 0), (-1, -1), 1.5, colors.black)
    ]))
    story.append(t1)
    #

    for i, key in enumerate(tabela):
        iteracija = str(i+1) + "."


        motivi = narocila_izdelka.filter(izdelek__skupina_izdelkov = key)
        print(motivi)
        data1 = [[Paragraph(iteracija, styles["Line_Data"]),
                Paragraph(key.koda, styles["Line_Data"]),
                Paragraph(key.ime, styles["Line_Data"]),
                Paragraph('', styles["Line_Data"]),
                Paragraph('', styles["Line_Data"])
                ]]

        t1 = Table(data1, colWidths=(1 * cm, 6 * cm,5 * cm,2.7*cm, 5 * cm))
        t1.setStyle(TableStyle([
            ('LINEBELOW', (0, 0), (-1, -1), 0.25, colors.black)
        ]))
        story.append(t1)

        for motiv in motivi:
            print(motiv)
            data1 = [[Paragraph('', styles["Line_Data"]),
                Paragraph('', styles["Line_Data"]),
                Paragraph('', styles["Line_Data"]),
                Paragraph(motiv.izdelek.koda, styles["Line_Data"]),
                Paragraph(str(motiv.kolicina), styles["Line_Data"])
                ]]
            t1 = Table(data1, colWidths=(1 * cm, 6 * cm,5 * cm,2.7*cm, 5 * cm))
            t1.setStyle(TableStyle([
                ('LINEBELOW', (0, 0), (-1, -1), 0.25, colors.black)
            ]))
            story.append(t1)


        data1 = [[Paragraph('', styles["Line_Data"]),
                Paragraph('Skupaj', styles["Line_Data"]),
                Paragraph('', styles["Line_Data"]),
                Paragraph('', styles["Line_Data"]),
                Paragraph(str(tabela[key]), styles["Line_Data"])
                ]]
        t1 = Table(data1, colWidths=(1 * cm, 6 * cm,5 * cm,2.7*cm, 5 * cm))
        t1.setStyle(TableStyle([
            ('LINEBELOW', (0, 0), (-1, -1), 1.5, colors.black)
        ]))
        story.append(t1)

    return story

