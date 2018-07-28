from django.http import HttpResponse, HttpResponseRedirect,JsonResponse , HttpResponseForbidden
from django.core.paginator import Paginator
from django.template import loader
from django.shortcuts import render, redirect
from django.contrib import auth
from products.models import Kosarica
from django.template.context_processors import csrf
import datetime


def login(request):

	if is_admin(request):
		return HttpResponseRedirect("/narocila/nova_narocila/")

	context = {}
	error = request.session.pop('errorlogin', False)
	
	if error:
		context.update({'error': 'True'})
	

	return render(request, 'registration/login.html', context)


def logout(request):
	

	if is_normal_user(request):
		kosarica_uporabnika = Kosarica.objects.get(uporabnik__user = request.user)
		kosarica_uporabnika.narocila_izdelka.clear()

	auth.logout(request)
	return HttpResponseRedirect('/prijava/')

def auth_login(request):

	username = request.POST.get('usr', '')
	password = request.POST.get('pwd', '')
	user = auth.authenticate(username=username, password=password)

	if user is not None:
		auth.login(request, user)
		return HttpResponseRedirect('/')

	request.session['errorlogin'] = True
	return redirect( '/prijava/')


def is_logged_in(request):
	return request.user.is_authenticated

def is_admin(request):
	return request.user.is_authenticated and request.user.is_staff;

def is_normal_user(request):
	return request.user.is_authenticated and not request.user.is_staff;