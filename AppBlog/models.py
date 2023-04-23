from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.mixins import UserPassesTestMixin



class Autos(models.Model):
   
  marca = models.CharField(max_length=40)
  modelo = models.CharField(max_length=40)
  año_de_fabricacion = models.IntegerField()
  descripcion = models.TextField(max_length=240, null=True, blank=True)
  imagen = models.ImageField(upload_to='imagenautos', null=True, blank=True)
  fecha_de_edicion = models.DateField()
  version = models.CharField(max_length=30)
  motorizacion = models.CharField(max_length=30)
  combustible = models.CharField(max_length=30)
  usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

  def __str__(self):

    return f" {self.marca} {self.modelo}"


class Avatar(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='avatares', null=True, blank=True)

class EditarAutos(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
  model = Autos
  success_url = "/AppBlog/listaAutos"
  fields = ["marca", "modelo", "version", "año_de_fabricacion", "motorizacion", "combustible", "descripcion", 'imagen']
  template_name = "AppBlog/edicionAutos.html"

  def test_func(self):
    auto = self.get_object()
    return auto.user == self.request.user or self.request.user.is_superuser


class EliminarAutos(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
  model = Autos
  success_url = "/AppBlog/listaAutos"
  template_name = "AppBlog/eliminarautos.html"

  def test_func(self):
    auto = self.get_object()
    return auto.user == self.request.user or self.request.user.is_superuser
    
