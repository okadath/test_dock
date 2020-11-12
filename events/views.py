from django.shortcuts import render, render_to_response,redirect
from django.urls import reverse, reverse_lazy
from django.template import loader
from django.http import HttpResponse
from django.utils.timezone import now

from events.models import Note, Event,Event_User,Room,LivePlayer,Chat,Announcement,Video,Resource,Speaker, Programme, ProgrammeElement
from events.models import *
from events.forms import NoteForm#,PostAdminForm
from user_account.models import Code
from django.http import HttpResponseRedirect, HttpResponse


import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
import weasyprint
from weasyprint import HTML
from django.template.loader import get_template
from django.template import Template
from django.contrib.auth.decorators import login_required

# from django_weasyprint import WeasyTemplateResponseMixin

@login_required(login_url="/")
def create_pdf(request,title):
	# Create a file-like buffer to receive PDF data.
	# print(request.POST)
	buffer = io.BytesIO()
	try:
		actual_note=get_object_or_404(Note, title=title, user=request.user)
	# si title no existe regresa al main de notas
	except Exception as e: 
		form = NoteForm()
		return HttpResponseRedirect(reverse('notes'))
	b=str(actual_note.text)
	# print(b)
	# a='&lt;p&gt;aaaaaaaaaaaaaaa&lt;/p&gt;'
	# b="<p>aaaaaaaaaaaaaaa</p><br>pa"
	html_template=b.encode()
	pdf_file = weasyprint.HTML(string=html_template).write_pdf(buffer)
	buffer.seek(io.SEEK_SET)
	return FileResponse(buffer, as_attachment=True, filename=title+'.pdf')



from django.shortcuts import get_list_or_404, get_object_or_404

# # lista todos los eventos y los mios para despelgarlos
# @login_required(login_url="/")
# def all_events(request):
# 	ev = Event.objects
# 	try:
# 		my_events=Event_User.objects.filter (user=request.user ) 
# 	except Exception as e:
# 		my_events="" 
# 	return render(request, 'events/all_events.html', {'events': ev, "my_events":my_events} )



@login_required(login_url="/")
def support(request, slug):
	datos_evento = get_object_or_404(Event, slug=slug) 
	chat = Chat.objects.get(id=2)
	live_del_evento=LivePlayer.objects.get(event=datos_evento)
	return render(request, 'spa/app/event/dashboard/support.html', {"chat": chat, "event": datos_evento, "live":live_del_evento})


#este es el lobby inicial, sin haber dado click a las paginas laterales, no hay token que indique a donde ir
@login_required(login_url="/")
def see_event(request,slug):
	datos_evento=get_object_or_404(Event, slug=slug) 
	live_del_evento=LivePlayer.objects.get(event=datos_evento)
	chat_event=Chat.objects.get(event=datos_evento)
	date_now = now()
	lobby_message = 'Bienvenido a La Cumbre Global del Liderazgo'
	programme = Programme.objects.get(event=datos_evento)
	programme_elements = ProgrammeElement.objects.filter(programme=programme).order_by('place_in_programme')
	sponsors = Sponsor.objects.all().order_by('?')
	# ==========================emergency query=======================
	# en condiciones normales no deberia haber esto, pero si necesitas llamar a toda la info de todos los modelos de este evento acabo
	# de agregar esta parte para pasarlos directamente por en contexto
	# el precio de usar esto es que deber recargar la pagina para acceder a las notas, desde aqui no hay editor de notas
	# solo puedes leer las ya existentes e imprimirlas

	# rooms_del_evento=Room.objects.filter(event=datos_evento) 
	# anunc=Announcement.objects.filter(event=datos_evento)  
	# spek=Speaker.objects.filter(event=datos_evento) 
	# prog=Video.objects.filter(event=datos_evento)   
	# notes=Note.objects.filter(user=request.user) 
	# =================================================================
	return render(request, 'spa/app/event/dashboard/lobby.html',
				  {"event":datos_evento, 'lobby_message': lobby_message, "date_now":date_now, "live":live_del_evento,
				   "chat":chat_event, "programme_elements": programme_elements, "sponsors": sponsors} )
	# return render(request, 'spa/app/event/dashboard/lobby.html', 
	# 	{"event":datos_evento,"lives":live_del_evento,"chat":chat_event,
	# 	"my_rooms":rooms_del_evento,"announce":anunc,"program":prog,"speakers":spek,'notes': notes, } )


@login_required(login_url="/")
def rooms(request,slug):
	# print("editor")
	try:
		datos_evento=get_object_or_404(Event, slug=slug)   
	except Exception as e: 
		return render(request, 'events/lobby.html', {"event":datos_evento,"token":"room"} )
	rooms_del_evento=Room.objects.filter(event=datos_evento)
	live_del_evento=LivePlayer.objects.get(event=datos_evento)
	# notas_usuario=Note.objects.filter(user=request.user)  

# si necesitas pasarle los videos descomenta esto, agregale al render la key "videos":prog, y usa el html de program
	# prog=Video.objects.filter(event=datos_evento)  
	chat_event=Chat.objects.filter(event=datos_evento) 
	return render(request, 'spa/app/event/dashboard/rooms.html', {'event': datos_evento, "token":"room","my_rooms":rooms_del_evento, "live":live_del_evento,"chat":chat_event,} )


@login_required(login_url="/")
def room(request,slug,slug_room=""):
	try:
		datos_evento=get_object_or_404(Event, slug=slug)
	except Exception as e:
		return render(request, 'events/lobby.html', {"event":datos_evento,"token":"room"} )
	date_now = now()
	room_del_evento=Room.objects.get(slug=slug_room)
	live_del_evento=LivePlayer.objects.get(event=datos_evento)
	notes=Note.objects.filter(user=request.user) 
	chat_event=Chat.objects.get(event=datos_evento)
	sponsors = Sponsor.objects.all().order_by('?')
	# print(notes)
	if request.method == "POST":
		Note.objects.create(title=str(request.POST["title"]).replace("/", "_"),text=request.POST["text"],user=request.user) 
		notes=Note.objects.filter(user=request.user) 
		# print('guardado')
		return render(request, 'spa/app/event/dashboard/room.html', {"date_now": date_now, 'event': datos_evento, "token":"room","my_room":room_del_evento, "lives":live_del_evento,"chat":chat_event ,"notes":notes,} )
	else:
		notes=Note.objects.filter(user=request.user) 

	# si necesitas pasarle los videos descomenta esto, agregale al render la key "videos":prog, y usa el html de program
	# prog=Video.objects.filter(event=datos_evento)


	return render(request, 'spa/app/event/dashboard/room.html', {"date_now": date_now, 'event': datos_evento, "token":"room","my_room":room_del_evento, "lives":live_del_evento,"chat":chat_event ,"notes":notes, "sponsors":sponsors,} )


@login_required(login_url="/")
def programa(request,slug ):
	try:
		datos_evento=get_object_or_404(Event, slug=slug)
	except Exception as e: 
		return render(request, 'events/lobby.html', {"event":datos_evento,"token":"programa"})#, "lives":live_del_evento,"chat":chat_event} ) 
	live_del_evento=LivePlayer.objects.get(event=datos_evento)
	chat_event=Chat.objects.filter(event=datos_evento)  
	prog=Video.objects.filter(event=datos_evento)
	programme = Programme.objects.get(event=datos_evento)
	programme_elements = ProgrammeElement.objects.filter(programme=programme).order_by('place_in_programme')
	live_del_evento=LivePlayer.objects.get(event=datos_evento)

	# print(anunc)
	return render(request, 'spa/app/event/dashboard/schedule.html',
				  {'event': datos_evento, "token":"programa","program":prog, "lives":live_del_evento,"chat":chat_event,
				   "programme_elements":programme_elements, "live":live_del_evento} )


@login_required(login_url="/")
def recursos(request,slug ):
	try:
		datos_evento=get_object_or_404(Event, slug=slug)
	except Exception as e: 
		return render(request, 'events/lobby.html', {"event":datos_evento,"token":"recursos"})#, "lives":live_del_evento,"chat":chat_event} ) 
	chat_event=Chat.objects.filter(event=datos_evento)
	rec=Resource.objects.filter(event=datos_evento)
	live_del_evento=LivePlayer.objects.get(event=datos_evento)
	# print(anunc)
	return render(request, 'spa/app/event/dashboard/resources.html', {'event': datos_evento, "token":"recursos","recursos":rec, "live":live_del_evento,"chat":chat_event, "live":live_del_evento} )


@login_required(login_url="/")
def speaker(request,slug ,slug_speak=""):
	try:
		datos_evento=get_object_or_404(Event, slug=slug)
	except Exception as e: 
		return render(request, 'events/lobby.html', {"event":datos_evento,"token":"speakers"})#, "lives":live_del_evento,"chat":chat_event} )
	chat_event=Chat.objects.filter(event=datos_evento)
	live_del_evento=LivePlayer.objects.get(event=datos_evento)
	if slug_speak=="" :
		spek=Speaker.objects.filter(event=datos_evento)   
	else:
		spek=Speaker.objects.filter(slug=slug_speak)   
	return render(request, 'spa/app/event/dashboard/speakers.html', {'event': datos_evento, "token":"speakers","speakers":spek, "chat":chat_event, "live": live_del_evento} )


@login_required(login_url="/")
def delete_note(request,title,slug):
	notes=Note.objects.filter(user=request.user) 
	try:
		datos_evento=get_object_or_404(Event, slug=slug)
	except Exception as e: 
		return render(request, 'spa/app/event/dashboard/notes.html', {'notes': notes, "event":datos_evento,"token":"notes"}) 
	live_del_evento=LivePlayer.objects.get(event=datos_evento)
	chat_event=Chat.objects.filter(event=datos_evento) 
	
	try:
		actual_note=get_object_or_404(Note, title=title,user=request.user) 
	# si title no existe regresa al main de notas
	except Exception as e:  
		return render(request, 'spa/app/event/dashboard/notes.html', {'notes': notes, "event":datos_evento,"token":"notes"})
	# print("elimina")
	actual_note.delete()
	return HttpResponseRedirect(reverse('notes', args=[slug]))


@login_required(login_url="/")
def edit_note(request,title,slug):
	notes=Note.objects.filter(user=request.user) 
	try:
		datos_evento=get_object_or_404(Event, slug=slug)
	except Exception as e: 

		return render(request, 'spa/app/event/dashboard/notes.html', {'notes': notes, "event":datos_evento,"token":"notes"})#, "lives":live_del_evento,"chat":chat_event} ) 
	live_del_evento=LivePlayer.objects.get(event=datos_evento)
	chat_event=Chat.objects.filter(event=datos_evento)  
	try:
		actual_note=get_object_or_404(Note, title=title,user=request.user) 
	except Exception as e:  
		return render(request, 'spa/app/event/dashboard/notes.html', {'notes': notes, "event":datos_evento,"token":"notes","lives":live_del_evento,"chat":chat_event} ) 
	if request.method == "POST": 
		# hay un bug si el titulo es espacio vacio. corregir despues
		actual_note.title=str(request.POST["title"]).replace("/", "_")
		actual_note.text=request.POST["text"]
		actual_note.save() 
		# queda el nombre antiguo en la url, eso podria causar bugs, tengo que redirigir
		return HttpResponseRedirect(reverse('notes', args=[slug]))
	return render(request, 'spa/app/event/dashboard/notes.html', {'notes': notes, 'actual': actual_note, 'event': datos_evento, "token":"notes","lives":live_del_evento,"chat":chat_event} ) 


from django.contrib.auth.models import User


@login_required(login_url="/")
def notes(request,slug): 
	notes=Note.objects.filter(user=request.user)
	try:
		datos_evento=get_object_or_404(Event, slug=slug)
		live_del_evento=LivePlayer.objects.filter(event=datos_evento)
	except Exception as e:  
		return render(request, 'spa/app/event/dashboard/notes.html', {'notes': notes, "event":datos_evento,"token":"notes", "live": live_del_evento})#, "lives":live_del_evento,"chat":chat_event} )
	live_del_evento = LivePlayer.objects.get(event=datos_evento)
	chat_event=Chat.objects.filter(event=datos_evento)  
	us=User.objects.filter(username=request.user) 
	# notes=Note.objects.filter(user=request.user) 
	# print(request.POST)
	if request.method == "POST":
		Note.objects.create(title=str(request.POST["title"]).replace("/", "_"),text=request.POST["text"],user=request.user) 
		notes=Note.objects.filter(user=request.user) 
		print('guardado')
		return render(request, 'spa/app/event/dashboard/notes.html', {'notes': notes, "event":datos_evento,"token":"notes", "live":live_del_evento,"chat":chat_event} )
	else:
		notes=Note.objects.filter(user=request.user) 
	return render(request, 'spa/app/event/dashboard/notes.html', {'notes': notes, 'event': datos_evento, "token":"notes", "live":live_del_evento,"chat":chat_event} )




@login_required(login_url="/")
def user_guide(request,slug):
	context = {}
	try:
		datos_evento=get_object_or_404(Event, slug=slug)
	except Exception as e: 
		print("este evento o slug no existe!!el susario nunca deberia llegar aqui")
		# context["event"] = datos_evento
		# return render(request, 'spa/app/event/dashboard/user-guide.html', {"event":"no hay evento"})
	try:
		# actual_lang = get_object_or_404(Language, lang="English")
		# actual_userguide = get_object_or_404(UserGuideArticle, language=actual_lang)
		# obtiene la primer userguide, si tendran lang descomenta las lineas de arriba
		# y quita la de abajo
		actual_userguide =UserGuideArticle.objects.get(title="Guia de Usuario")
		# print(actual_userguide)
		context["title"] = actual_userguide.title
		a = actual_userguide.content.replace('<', ' ').replace('>', ' ').split()
		live_del_evento = LivePlayer.objects.get(event=datos_evento)
		context["content_string"] = actual_userguide.content
		context["content_url"] = a[3]
		context["event"] = datos_evento
		context["live"] = live_del_evento
		# me falta arreglar y definir esto y su url
		return render(request, 'spa/app/event/dashboard/user-guide.html', context)
	except Exception as e:
		context["event"] = datos_evento
		return render(request, 'spa/app/event/dashboard/user-guide.html', context)


@login_required(login_url="/")
def sponsors(request,slug ):
	context = {}
	try:
		datos_evento=get_object_or_404(Event, slug=slug)
		live_del_evento = LivePlayer.objects.get(event=datos_evento)
		context["event"] = datos_evento
		context["live"] = live_del_evento
	except Exception as e:
		print("error")
		# return render(request,'spa/app/event/dashboard/sponsor.html', {"event":datos_evento,"token":"recursos"})#, "lives":live_del_evento,"chat":chat_event} ) 
	# solo habra un evento, por eso busca todos, si no agregar pk event a Sponsor
	sponsors=Sponsor.objects.all()
	context["event"] = datos_evento
	context["sponsors"] = sponsors
	return render(request, 'spa/app/event/dashboard/sponsor.html', context)


from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.conf import settings
from events.tasks import enviar_mail
from events.forms import SupportForm


@login_required(login_url="/")
# name description image
def supportspiritual(request,slug):
	context = {}
	try:
		datos_evento=get_object_or_404(Event, slug=slug)
		live_del_evento = LivePlayer.objects.get(event=datos_evento)
		context["event"] = datos_evento
		context["live"] = live_del_evento
	except Exception as e:
		print("error")

	if request.method == 'POST':
		support_form = SupportForm(data=request.POST)
		if support_form.is_valid():
			supportForm = SupportForm(data=request.POST, files=request.FILES)
			support = support_form.save(commit=False)
			support.user = request.user
			try:
				support.image = request.FILES["image"]
			except Exception as e:
				support.image = ""
			support_form.save()

			texto_mail=request.POST["name"]+'\n'+request.POST["description"]
			asunto='Subject of the Email(TEST)'
			# msg = EmailMessage(, texto_mail, "admin@glsteamedition.com", settings.DESTINATARIOS_ORACION)
			# msg.content_subtype = "html"
			# msg.attach_file(settings.BASE_DIR+"/"+support.image.url)
			# msg.send()

			if support.image=="":
				enviar_mail.delay(asunto, texto_mail, settings.DESTINATARIOS_ORACION)
			else:
				enviar_mail.delay(asunto, texto_mail, settings.DESTINATARIOS_ORACION,support.image.url)

			context['form']=support_form
			context['messages']="Mensaje enviado, muchas gracias"
			return render(request, 'spa/app/event/dashboard/spiritualsupport.html',context)
		else:
			context['form']=support_form
			if request.POST["description"]=="":
				context['error_messages']="La descripcion no debe ir vacia"
				return render(request, 'spa/app/event/dashboard/spiritualsupport.html',context)
			context['error_messages']="Nombre repetido"
			return render(request, 'spa/app/event/dashboard/spiritualsupport.html',context)
	else:
		support_form = SupportForm()
		context['form']=support_form
	return render(request, 'spa/app/event/dashboard/spiritualsupport.html', context)


from events.forms import TeamEditionForm


@login_required(login_url="/")
# title content image
def teamedition(request,slug):
	context = {}
	try:
		datos_evento=get_object_or_404(Event, slug=slug)
		live_del_evento = LivePlayer.objects.get(event=datos_evento)
		context["event"] = datos_evento
		context["live"] = live_del_evento
	except Exception as e:
		print("error")

	if request.method == 'POST':
		form = TeamEditionForm(data=request.POST)
		if form.is_valid():
			supportForm = TeamEditionForm(data=request.POST, files=request.FILES)
			support = form.save(commit=False)
			# support.user = request.user
			try:
				support.image = request.FILES["image"]
				file_type = support.image.url.split('.')[-1]
				# print(file_type)
				file_type = file_type.lower()
				if file_type not in settings.IMAGE_FILE_TYPES:
					context['form']=form
					context['error_messages']="El tipo de archivo debe ser jpg,jpeg,png o pdf"
					return render(request, 'spa/app/event/dashboard/teamedition.html',context)
			except Exception as e:
				# raise e
				support.image = ""
			form.save()

			texto_mail=request.POST["title"]+'\n'+request.POST["content"]
			asunto='Subject of the Email(TEST)'
			# texto_mail=request.POST["title"]+'\n'+request.POST["content"]
			# msg = EmailMessage('Subject of the Email(TEST)', texto_mail, "admin@glsteamedition.com", settings.DESTINATARIOS_TE)
			# msg.content_subtype = "html"
			# msg.attach_file(settings.BASE_DIR+"/"+support.image.url)
			# msg.send()

			if support.image=="":
				enviar_mail.delay(asunto, texto_mail, settings.DESTINATARIOS_TE)
			else:
				enviar_mail.delay(asunto, texto_mail, settings.DESTINATARIOS_TE,support.image.url)

			context['form']=form
			context['messages']="Mensaje enviado, muchas gracias"
			return render(request, 'spa/app/event/dashboard/teamedition.html',context)
		else:
			context['form']=form
			#no se como se hace una validacion de no vacio
			if request.POST["content"]=="":
				context['error_messages']="El campo contenido no debe ir vacio"
				return render(request, 'spa/app/event/dashboard/teamedition.html',context)
			context['error_messages']="Nombre repetido"
			return render(request, 'spa/app/event/dashboard/teamedition.html',context)
	else:
		form = TeamEditionForm()
		context['form']=form
	return render(request, 'spa/app/event/dashboard/teamedition.html', context)


def privacy(request,slug=""):
	context={}
	try:
		datos_evento=get_object_or_404(Event, slug=slug)
		context["event"] = datos_evento
	except Exception as e: 
		pass
	priv =UserGuideArticle.objects.get(title="Privacidad")
	context["title"]=priv.title
	context["content_string"]=priv.content
	return render(request,"spa/app/event/pages/privacy.html",context)


def legal(request,slug=""):
	context={}
	try:
		datos_evento=get_object_or_404(Event, slug=slug)
		context["event"] = datos_evento
	except Exception as e: 
		pass
	legal =UserGuideArticle.objects.get(title="Legal")
	context["title"]=legal.title
	context["content_string"]=legal.content
	return render(request,"spa/app/event/pages/legal.html",context)
