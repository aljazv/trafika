from django.http import HttpResponse, HttpResponseRedirect,JsonResponse , HttpResponseForbidden
from django.core.paginator import Paginator
from django.template import loader
from django.shortcuts import render
import datetime

from products.views import *
from . import excel

from products.models import *
from trafika.views import *

# Create your views here.


def nova_narocila(request):

		if not is_logged_in(request):
					return HttpResponseRedirect("/prijava/")

		if is_normal_user(request):
				return HttpResponseRedirect("/")

		confirmed = False
		if request.method == 'POST' and 'narocilo_id2' in request.POST:
				narocilo_id = request.POST['narocilo_id2']
				narocilo = Narocilo.objects.get(id = narocilo_id)
				narocilo.je_obdelan = True
				narocilo.save()
				confirmed = True
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
			'narocila_neobdelano': narocila_neobdelano,
			'confirmed': confirmed
			}

		return render(request,'narocila/nova_narocila.html',context)


def spremeni(request, id):
		if not is_logged_in(request):
				return HttpResponseRedirect("/prijava/")

		if is_normal_user(request):
				return HttpResponseRedirect("/")

		error = None
		narocilo = Narocilo.objects.get(id=id)

		code = ""
		amount = ""

		if request.method == 'POST' and 'narocilo' in request.POST:
				kolicina = request.POST['kolicina']
				narocilo_izdelka_id = request.POST['narocilo']
				narocilo_izdelka = NarociloIzdelka.objects.filter(id = narocilo_izdelka_id)[0]
				narocilo_izdelka.kolicina = kolicina
				narocilo_izdelka.save()

		elif request.method == 'POST' and 'odstrani_izdelek_admin' in request.POST:

				narocilo_izdelka_id = request.POST['narocilo-izdelka-id']

				narocilo = Narocilo.objects.get(id=narocilo.id)

				narocilo_izdelka = NarociloIzdelka.objects.get(id = narocilo_izdelka_id)

				narocilo.narocila_izdelka.remove(narocilo_izdelka)

				narocilo_izdelka.delete()

		elif request.method == 'POST' and 'koda-input' in request.POST:

				code = request.POST['koda-input']
				amount = request.POST['kolicina']

				narocilo = Narocilo.objects.get(id=narocilo.id)

				try:
				    izdelek = Izdelek.objects.get(koda__iexact=code)

				    if narocilo.narocila_izdelka.filter(izdelek=izdelek).count() > 0:
				    	error = "Izdelek je že dodan v naročilu."
				    else:
					    narociloIzdelka = NarociloIzdelka(izdelek=izdelek, kolicina=amount)
					    narociloIzdelka.save()


					    narocilo.narocila_izdelka.add(narociloIzdelka)
				except Izdelek.DoesNotExist:
				    error = "Izdelek s kodo " + code + " ne obstaja."


		context = {
			"narocilo": narocilo,
			"error": error,
			"code": code,
			"amount": amount
		}
		return render(request,'narocila/spreminjanje_narocila.html',context)


def stara_narocila(request):

		if not is_logged_in(request):
				return HttpResponseRedirect("/prijava/")

		if is_normal_user(request):
				return HttpResponseRedirect("/")

		if request.method == 'POST' and 'prenesi_narocilnica' in request.POST:
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


		if request.method == 'POST' and 'uveljavi' in request.POST:
				narocilo_id = request.POST['narocilo_id']
				nacin_prodaje = request.POST['nacinProdaje']
				nacin_dostave = request.POST['nacinDostave']
				narocilo = Narocilo.objects.get(id = narocilo_id)
				narocilo.nacin_prodaje = nacin_prodaje
				narocilo.nacin_dostave = nacin_dostave
				narocilo.save()

		if request.method == 'POST' and 'prenesi_dobavnica' in request.POST:
				
				narocilo_id = request.POST['narocilo_id']
				narocilo = Narocilo.objects.get(id = narocilo_id)
				leto_dobavnice = narocilo.datum.strftime("%Y")
				st_dobavnice = leto_dobavnice[-2:] + str(narocilo.id).zfill(4)
				ime_datoteke = "dobavnica" + "_" + st_dobavnice + ".pdf"
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


		narocila_obdelano = Narocilo.objects.filter(je_obdelan = True).order_by('-datum')

		paginator = Paginator(narocila_obdelano, 15)
		page = request.GET.get('page')
		paginirana_narocila = paginator.get_page(page)

		context = {
				'narocila_obdelano': paginirana_narocila
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

		tabela = {x:y for x,y in tabela.items() if y!=0} #izbrises te k so 0!

		uporabnik = narocilo.uporabnik
		story = []

		formatted_time = datetime.date.today()
		formatted_time = str(formatted_time)
		tabela1 = formatted_time.split("-")
		formatted_time = tabela1[2] + "." + tabela1[1] + "." + tabela1[0]

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

		data1 = [[Paragraph('DOBAVNICA', styles["Line_Data_Largest"]),
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
							Paragraph('', styles["Line_Label"]),
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
							Paragraph(narocilo.potnik.uporabnik.user.first_name + " " + narocilo.potnik.uporabnik.user.last_name, styles["Line_Data_Large"])
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
						Paragraph('količina', styles["Line_Label"])
						]]
				
		t1 = Table(data1, colWidths=(1 * cm, 6 * cm,7.7 * cm, 5 * cm))
		t1.setStyle(TableStyle([
				('LINEBELOW', (0, 0), (-1, -1), 1.5, colors.black)
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
						

				t1 = Table(data1, colWidths=(1 * cm, 6 * cm,7.7 * cm,5 * cm))
				t1.setStyle(TableStyle([
						('LINEBELOW', (0, 0), (-1, -1), 0.25, colors.black)
				]))
				story.append(t1)

				#for motiv in motivi:
				#    print(motiv)
				#    data1 = [[Paragraph('', styles["Line_Data"]),
				#        Paragraph('', styles["Line_Data"]),
				#        Paragraph('', styles["Line_Data"]),
				#        Paragraph(motiv.izdelek.koda, styles["Line_Data"]),
				#        Paragraph(str(motiv.kolicina), styles["Line_Data"])
				#        ]]
				#    t1 = Table(data1, colWidths=(1 * cm, 6 * cm,5 * cm,2.7*cm, 5 * cm))
				#    t1.setStyle(TableStyle([
				#        ('LINEBELOW', (0, 0), (-1, -1), 0.25, colors.black)
				#    ]))
				#    story.append(t1)


				#data1 = [[Paragraph('', styles["Line_Data"]),
				#        Paragraph('Skupaj', styles["Line_Data"]),
				#        Paragraph('', styles["Line_Data"]),
				#        Paragraph('', styles["Line_Data"]),
				#        Paragraph(str(tabela[key]), styles["Line_Data"])
				#        ]]
				#t1 = Table(data1, colWidths=(1 * cm, 6 * cm,5 * cm,2.7*cm, 5 * cm))
				#t1.setStyle(TableStyle([
				#    ('LINEBELOW', (0, 0), (-1, -1), 1.5, colors.black)
				#]))
				#story.append(t1)

		return story

