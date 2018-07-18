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
        #list vseh imen skupine izdelkov + filas, ce je nakonc ksn nic ga ne das na dobavnico. Hash table,dictionary

        narocilo_id = request.POST['narocilo_id']
        narocilo = Narocilo.objects.get(id = narocilo_id)
        ime_datoteke = "dobavnica" + str(narocilo.id) + ".pdf"
        story=[]
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="{}"'.format(ime_datoteke)
        doc = SimpleDocTemplate(response,pagesize=letter,
            rightMargin=20,leftMargin=20,
            topMargin=20,bottomMargin=20)

        story = natisni_narocilnica(request,narocilo)
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


def natisni_dobavnica(request,narocilo):
    narocila_izdelka = narocilo.narocila_izdelka.all()
    #prestejes za skupino izdelkov!!


    uporabnik = Uporabnik.objects.get(user = request.user)
    story = []

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
                Paragraph("", styles["Line_Data"])
                ]]

        t1 = Table(data1, colWidths=(1 * cm, 3.6 * cm, 5 * cm, 5 * cm, 3 * cm, 1.6 * cm, 0.8 * cm))
        t1.setStyle(TableStyle([
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        story.append(t1)

    return story