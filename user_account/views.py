from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
# from user_account.forms import SignupForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse, reverse_lazy
from events import views as view_events
from user_account.models import Code,User_Code #,Profile
from django.shortcuts import get_list_or_404, get_object_or_404
from user_account.forms import UserForm
from events.views import  see_event
from django.contrib.auth.decorators import login_required


def home(request):
	return render(request, 'home.html')


def logout_view(request):
	logout(request) 
	return redirect('login_mail')


#no se cual sera tu main page, puse esta por si acaso
def dashboard(request):
	return render(request, 'user_account/dashboard.html')

@login_required(login_url="/")
def lobby(request):
    # como lo hardcodeamos aqui va un evento, tiene que ir a un menu de eventos accesibles por slug
    # aqui le pasamos el slug
    # see_event(request,"gls-online")
    room(request,"gls-online","1-Programming")
    # return render(request, 'user_account/dashboard.html')

from user_account.auth_backend import PasswordlessAuthBackend

def  login_code(request): 
    if request.method == 'POST':
        cod = request.POST.get('code') 
        try:
            exist_code = Code.objects.get(code=cod) 
            try: 
                username = get_object_or_404(User_Code, code=exist_code.id).user.username
                print(username)
            except Exception as e:
                return render(request, 'user_account/login_code.html', {
                    "error_messages":
                        'This code has no user'})
        except Exception as e: 
            return render(request, 'user_account/login_code.html', {
                "error_messages":
                    'Invalid code'})
        # print(username)
        user = PasswordlessAuthBackend.authenticate(user=username)
        # print(user)
        # print(user.username)
        # print(user.email)
        if user:
            if user.is_active:
                login(request, user, backend='user_account.auth_backend.PasswordlessAuthBackend')
                return HttpResponseRedirect(reverse('see_event', kwargs={'slug':"gls-online"}))
                # return HttpResponseRedirect(reverse('dashboard'))
            else:
                return render(request, 'user_account/login_code.html', {
                    "error_messages":
                        'Account Inactive'})
        else: 
            return render(request, 'user_account/login_code.html', {
                "error_messages":
                    'Incorrect data'})

    else:
        return render(request, 'user_account/login_code.html', {})

# new_user = User.objects.create_user(username, email, password)
# new_user.is_active = False
# new_user.first_name = first_name
# new_user.last_name = last_name
# new_user.save()

def register_user(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('event/lobby/gls-online/')
    
    if request.method == 'POST':
        # print(request.POST)
        # print(request.POST.get('email')  )
        mail=request.POST.get('email') 
        a=mail.split("@")
        # hardcoded validation, cuando haya mas codigos este if se comenta o borra o se llama al ORM!
        if str(request.POST.get('password')) !="entrenamientoCGL20" :
            user_form = UserForm()
            return render(request, 'spa/app/event/pages/register.html', {'user_form': user_form,  'error_messages': "Error:¡Codigo incorrecto!" })
       
        if request.POST.get('email') =="" or request.POST.get('first_name')=="" or request.POST.get('last_name')=="" :
            user_form = UserForm()
            return render(request, 'spa/app/event/pages/register.html', {'user_form': user_form,  'error_messages': "Error:¡Llenar todos los campos!" })
        user_form = UserForm(data=request.POST)
        if user_form.is_valid(): 
            try:
                a=get_object_or_404(User,username=a[0])
                user_form = UserForm()
                return render(request, 'spa/app/event/pages/register.html', {'user_form': user_form,  'error_messages': "Error:¡Este correo ya existe!" })
       
            except Exception as e: 
                user = user_form.save()
                user.username=a[0] 
                user.set_password("alpha2020")#user.password)
                u = user.save()
                # print(u)
                login(request, user, "django.contrib.auth.backends.ModelBackend")
                return HttpResponseRedirect(reverse('see_event', kwargs={'slug':"gls-online"}))
        else:
            # print(user_form)
            # return  HttpResponseRedirect( reverse_lazy('user_tradicional:update_profile'), { 'registered':registered})
            print(user_form.errors)
        # return HttpResponseRedirect(reverse('error404'))
    else:
        user_form = UserForm()
    # return render(request, 'user_account/signin.html', {'user_form': user_form,   })

    return render(request, 'spa/app/event/pages/register.html', {'user_form': user_form,   })


from django.contrib.auth.forms import AuthenticationForm
def login_mail(request):
    form = AuthenticationForm()
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('room', kwargs={'slug':"gls-online",'slug_room':"1-Programming"}))
    if request.method == 'POST':
        print(request.POST) 
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            # Recuperamos las credenciales validadas
            username = form.cleaned_data['username']
            password = form.cleaned_data['password'] 
            user = authenticate(username=username, password=password) 
            if user:
                if user.is_active:
                    login(request, user)
                    # return HttpResponseRedirect(reverse('see_event', kwargs={'slug':"gls-online"}))#args='Conferencia Alpha Online'))
                    return HttpResponseRedirect(reverse('room', kwargs={'slug':"gls-online",
                                                                        'slug_room':"1-Programming"}))#args='Conferencia Alpha Online'))                
                else:
                    return render(request, 'spa/app/event/pages/login.html', {"form":form,
                        "error_messages": 'El acceso estará disponible el 29 de Octubre a las 18:00 hrs'})
            else:
                return render(request, 'spa/app/event/pages/login.html', {"form":form,
                    "error_messages":'El acceso estará disponible el 29 de Octubre a las 18:00 hrs'})
        return render(request, 'spa/app/event/pages/login.html', {"form":form,
                        "error_messages": 'El acceso estará disponible el 29 de Octubre a las 18:00 hrs'})
    else:
        return render(request, 'spa/app/event/pages/login.html', {"form":form})
