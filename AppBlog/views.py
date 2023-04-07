from datetime import date
from django.shortcuts import render
from .models import *
from .forms import *
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, DeleteView
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.views import LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

def inicio(request):      #funcion para mostrar el inicio

    return render (request, 'AppBlog/inicio.html')



def aboutinfo (request):     #funcion para mostrar la información "acerca de"

    return render (request, 'AppBlog/about.html')


@login_required
def formularioAutos(request):   #funcion para mostrar el formulario para ingresar autos

    if request.method == 'POST':

        form = FormuAutos(request.POST, request.FILES)

        if form.is_valid():

            info = form.cleaned_data

            auto = Autos(marca=info['marca'], modelo=info['modelo'], año_de_fabricacion=info['año_de_fabricacion'], descripcion=info['descripcion'], fecha_de_edicion=date.today(), imagen=info['imagen'], version=info['version'], motorizacion=info['motorizacion'], combustible=info['combustible'])

            auto.save()

            return render (request, "AppBlog/inicio.html")

    else:

        form = FormuAutos()

    return render (request, 'AppBlog/formuautos.html', {"form": form})


@login_required
def busquedaAutos(request):     #funcion para mostrar formulario para buscar autos

    return render(request, "AppBlog/busqueda.html")


@login_required
def resultadoBusqueda(request):     #funcion para mostrar el resultado de la busqueda

    if request.GET['marca']:

        marca = request.GET['marca']

        auto = Autos.objects.filter(marca__icontains=marca)

        return render (request, 'AppBlog/resultadoBusq.html', {"auto": auto, "marca": marca})

    else:
        
        return render(request, 'AppBlog/error.html',)



def error(request):    #funcion para mostrar error al no ingresar datos en al busqueda

    return render(request, 'AppBlog/error.html')



class ListarAutos(ListView):        #clase para listar autos

    model = Autos
    template_name = "AppBlog/listaAutos.html"



class DetalleAutos(DetailView):      #clase para mostrar detalles

    model = Autos
    template_name = "AppBlog/detalleAutos.html"



class EditarAutos(LoginRequiredMixin, UpdateView):        #clase para editar los autos

    model = Autos
    success_url = "/AppBlog/listaAutos"
    fields = ["marca", "modelo", "version", "año_de_fabricacion", "motorizacion", "combustible", "descripcion", 'imagen']
    template_name = "AppBlog/edicionAutos.html"



class EliminarAutos(LoginRequiredMixin, DeleteView):

    model = Autos
    success_url = "/AppBlog/listaAutos"
    template_name = "AppBlog/eliminarautos.html"



def login_request(request):      #funcion para el login

    if request.method == 'POST':

        form = AuthenticationForm(request, data = request.POST)

        if form.is_valid():

            usuario = form.cleaned_data.get('username')
            contra = form.cleaned_data.get('password')

            user = authenticate(username = usuario, password = contra)

            if user:

                login(request, user)

                return render(request, "AppBlog/inicio.html", {"mensaje": f"Bienvenido {user}"})
        
        else:

            return render (request, "AppBlog/inicio.html", {"mensaje": "Error en los datos ingresados."})

    else:

        form = AuthenticationForm()

    return render (request, "AppBlog/login.html", {"form": form})



def register(request):     #funcion para crear registro

    if request.method == "POST":

        form = FormuRegisitro(request.POST)

        if form.is_valid():

            username = form.cleaned_data['username']
            
            form.save()

            return render (request, "AppBlog/inicio.html", {"mensaje": "Usuario creado con éxito"})

    else:

        form = FormuRegisitro()

    return render (request, "AppBlog/registro.html", {"form": form})



def editarUsuario(request):   #funcion para editar el usuario

    usuario = request.user

    if request.method == 'POST':

        miFormu = EditarUsuario(request.POST)

        if miFormu.is_valid():

            info = miFormu.cleaned_data

            usuario.email = info['email']
            usuario.first_name = info['first_name']
            usuario.last_name = info['last_name']
            usuario.password1 = info['password1']
            usuario.password2 = info['password2']

            usuario.save()

            return render (request, "AppBlog/inicio.html")

    else:

        miFormu = EditarUsuario(initial={'first_name':usuario.first_name, 'last_name': usuario.last_name, 'email': usuario.email})

    return render (request, "AppBlog/editarUsuario.html", {"miFormu": miFormu, "usuario": usuario})



@login_required
def agregarAvatar(request):    #Función para agregar foto al perfil del usuario

    if request.method == 'POST':

        miFormu = FormuAvatar(request.POST, request.FILES)

        if miFormu.is_valid():

            usuario = User.objects.get(username=request.user)

            avatar = Avatar (user=usuario, imagen=miFormu.cleaned_data['imagen'])

            avatar.save()

            return render(request, "AppBlog/inicio.html")

    else:

        miFormu = FormuAvatar()

    return render (request, 'AppBlog/agregarAvatar.html', {"miFormu": miFormu})



