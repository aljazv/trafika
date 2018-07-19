from django.http import HttpResponse, HttpResponseRedirect,JsonResponse , HttpResponseForbidden
from django.core.paginator import Paginator
from django.template import loader
from django.shortcuts import render
import datetime

from products.views import *

from products.models import *
# Create your views here.


def nova_narocila(request):
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

def stara_narocila(request):

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


def natisni_dobavnica(request, narocilo):
    narocila_izdelka = narocilo.narocila_izdelka.all()
    #prestejes za skupino izdelkov!!
    #list vseh imen skupine izdelkov + filas, ce je nakonc ksn nic ga ne das na dobavnico. Hash table,dictionary
    skupineIzdelkov = SkupinaIzdelkov.objects.all()
    
    tabela = dict((skupina,0) for skupina in skupineIzdelkov)
    
    for narocilo_izdelka in narocila_izdelka:
        tabela[narocilo_izdelka.izdelek.skupina_izdelkov] += narocilo_izdelka.kolicina
    

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
    p4 = styles.add(ParagraphStyle(name='Line_Data',fontName='Vera', alignment=TA_LEFT, fontSize=11, leading=13))
    p5 = styles.add(ParagraphStyle(name='Line_Data_Small',fontName='Vera', alignment=TA_LEFT, fontSize=7, leading=8))
    p6 = styles.add(ParagraphStyle(name='Line_Data_Large',fontName='Vera', alignment=TA_LEFT, fontSize=12, leading=13))
    p7 = styles.add(ParagraphStyle(name='Line_Data_Largest',fontName='Vera', alignment=TA_LEFT, fontSize=14, leading=15))
    p8 = styles.add(ParagraphStyle(name='Line_Label',fontName='Vera', font='Helvetica-Bold', fontSize=7, leading=6, alignment=TA_LEFT))
    p9 = styles.add(ParagraphStyle(name='Line_Label_Center',fontName='Vera', font='Helvetica-Bold', fontSize=7, alignment=TA_CENTER))
    

    ptext = '<font size=12>%s</font>' % formatted_time
    par = Paragraph(ptext, p0)
    story.append(par)
    story.append(Spacer(1, 12))
 
    # prodajno mesto + podjetje
    podjetje = uporabnik.podjetje
    prodajno_mesto = uporabnik.prodajno_mesto

    podjetje_podatki = '%s <br/> %s <br/> %s, %s <br/> %s <br/> ' % (podjetje.ime, podjetje.naslov, podjetje.postna_stevilka, podjetje.obcina, podjetje.davcna_stevilka)
        
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
    story.append(Spacer(1, 20))
    #
    story.append(Paragraph("DOBAVNICA", styles["Line_Label_Center"]))
    #
    datum = narocilo.datum.strftime("%d.%m.%Y, %H:%M")
    leto_dobavnice = narocilo.datum.strftime("%Y")
    st_dobavnice = leto_dobavnice[-2:] + str(narocilo.id).zfill(4)

    data1 = [[Paragraph('ŠTEVILKA DOBAVNICE', styles["Line_Label"]),
              Paragraph('DATUM NAROČILA', styles["Line_Label"])],

            [Paragraph(st_dobavnice, styles["Line_Data_Largest"]),
             Paragraph(datum, styles["Line_Data_Largest"])
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

    data1 = [[Paragraph('NAČIN DOSTAVE', styles["Line_Label"]),
                Paragraph('NAČIN PRODAJE', styles["Line_Label"])],

                [Paragraph(narocilo.nacin_prodaje, styles["Line_Data_Large"]),
                Paragraph(narocilo.nacin_dostave, styles["Line_Data_Large"])]
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
    potnik = narocilo.potnik
    potnik_podatki = '%s %s <br/> %s <br/> %s ' % (potnik.user.first_name, potnik.user.last_name, potnik.telefon, potnik.email)

    data1 = [[Paragraph('POTNIK', styles["Line_Label"])],
            [Paragraph(potnik_podatki, styles["Line_Data"])
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
    data1 = [[Paragraph('št', styles["Line_Label"]),
            Paragraph('črtna koda EAN', styles["Line_Label"]),
            Paragraph('artikel', styles["Line_Label"]),
            Paragraph('količina', styles["Line_Label"])
            ]]
        
    t1 = Table(data1, colWidths=(1 * cm, 7.7 * cm,6 * cm, 5 * cm))
    t1.setStyle(TableStyle([
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(t1)
    #

    for i, key in enumerate(tabela):
        iteracija = str(i+1) + "."
        
        data1 = [[Paragraph(iteracija, styles["Line_Data"]),
                Paragraph(key.koda, styles["Line_Data"]),
                Paragraph(key.ime, styles["Line_Data"]),
                Paragraph(str(tabela[key]), styles["Line_Data"])
                ]]

        t1 = Table(data1, colWidths=(1 * cm, 7.7 * cm,6 * cm, 5 * cm))
        t1.setStyle(TableStyle([
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        story.append(t1)

    return story