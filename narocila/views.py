from django.http import HttpResponse, HttpResponseRedirect,JsonResponse , HttpResponseForbidden
from django.core.paginator import Paginator
from django.template import loader
from django.shortcuts import render
import datetime

from .models import *
# Create your views here.

def nova_narocila(request):

    narocila = Narocilo.objects.filter(je_obdelan = False)

    context = {
        'narocila': narocila
        }

    return render(request,'narocila/nova_narocila.html',context)