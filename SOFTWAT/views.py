
from http.client import HTTPResponse
import re
from urllib import request
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth import authenticate
from django.contrib import messages
from GestionProductos.models import Product
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponse

#para enviar emails y que las funciones sirvan en views
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings

from SOFTWAT.forms import UserRegisterForm

def paginaprincipal(request):
    return render(request,'PAGINA_PRINCIPAL.HTML',{
        #context
    })

def ClienteInicio(request):

    if request.method == "GET":
        return render(request,'cliente_inicio.html',{
        "form" : UserCreationForm
        #context
    })
    


def Mision(request):
    return render(request,'Mision.html',{
        #context
    })

def CatPinturas(request):

    products = Product.objects.all().order_by(-id)

    return render(request,'PINTURAS.HTML',{
        'message': 'Productos',
        'name': 'productos',
        'products': products,
    })

def CatRollos(request):
    return render(request,'ROYOS.HTML',{
        #context
    })

def Aplicacion(request):
    return render(request,'APLICACION.HTML',{
        #context
    })

# Domicilios
def Domicilio(request):
    return render(request,'Seleccione.html',{
        #context
    })

def Estado(request):
    return render(request,'Estado.html',{

    })

def Actualizar(request):
    return render(request,'ActualizarDomi2.html',{

    })

# ----------------------------------------

# def Carrito(request):
#     return render(request,'VENTAS.HTML',{
#         #context
#     })

# LOGIN
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, 'Bienvenido {}'.format(user.username))
            return redirect('index')
        else: 
            messages.error(request, 'Usuario o contraseña incorrectos')
    return render(request, 'login.html',{

    })


def PQRS(request):
    return render(request,'PQRS.html',{
     #context
    })

#funcion para renderisar las funciones del email
def PQRS(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']
        
        template = render_to_string('email_template.html', {
            'name': name,
            'email': email,
            'message': message
        })
    #consolidacion de nuestro correo electronico
    #nos va a trar subject y luego lo que hay en email_TEMPLATE
    # y la configuracion de settings.email_host_user que hay que implementar
        email = EmailMessage(
            subject,
            template,
            settings.EMAIL_HOST_USER,
            ['holman10025@gmail.com']
        )
    
        email.fail_silently = False
        email.send()
    
    return render(request, 'PQRS.html',{

    })

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            messages.success(request, f'Usuario{username}creado ')
            return redirect('login')
    else:
        form= UserRegisterForm()

    context = {'form' : form} 
    return render(request, 'cliente_inicio.html', context)

#logout
def logout_view(request):
    logout(request)
    messages.success(request, 'Sesion Cerrada')
    return redirect('login')
