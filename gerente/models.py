from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin, BaseUserManager)
from django.contrib.auth.models import AbstractUser

# Modelos de la base de datos

class Departamento (models.Model):
    """
    Modelo que representa la tabla en la BD de Departamentos en los que trabajan los usuarios
    """
    nombre = models.CharField('Nombres', max_length=100)

    def __str__(self):
        """
        Representación en un String del departamento
        """
        return f"Departamento: {self.nombre}"

class TipoViatico(models.Model):
    """
    Modelo que representa los tipos de viaticos, es un catalogo.
    """
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre
    
class UserProfileManager(BaseUserManager):
    """ Manager del Modelo de Perfil de Usarios """

    def create_user(self, email, name, apellidos, password=None):
        """ Crear nuevo UserProfile"""
        if not email:
            raise ValueError('Usuario debe tener un email')
        
        email = self.normalize_email(email)
        user  = self.model(email=email, name=name, apellidos=apellidos)

        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_superuser(self, email, name, apellidos, password):
        """ Crear un Super Usuario"""
        user              = self.create_user(email, name, apellidos, password)
        user.is_superuser = True
        user.is_staff     = True

        user.save(using=self._db)

        return user
    
class UserProfile(AbstractBaseUser, PermissionsMixin):
    """ Modelo Base de datos para Usuarios en el Sistema """
    email     = models.EmailField('Email', max_length=255, unique=True)
    name = models.CharField('Nombres', max_length=100)
    apellidos = models.CharField('Apellidos', max_length=100)
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE, null=True)
    is_active = models.BooleanField(default=True)
    is_staff  = models.BooleanField(default=True)

    class Meta:
        swappable = 'AUTH_USER_MODEL'

    class Meta(AbstractUser.Meta):
        pass

    objects = UserProfileManager()

    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = ['name', "apellidos"]

    def get_full_name(self):
        ''' Obtener nombre completo del usuario'''
        return self.name

    def get_short_name(self):
        ''' Obtener nombre corto del usuario '''
        return self.name

    def __str__(self):
        ''' Obtener cadena representativa de nuestro usuario '''
        return self.email

class Evento(models.Model):
    """
    Modelo que representa los eventos a los que iran los empleados y necesitaran tener un detalle de sus gastos.
    """
    nombre = models.CharField('Nombre', max_length=50)
    lugar = models.CharField(max_length=100)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()

    def __str__(self):
        ''' Obtener cadena representativa de nuestro usuario '''
        return self.lugar

class AsistenciaEvento(models.Model):
    """
    Modelo que representa la relación muchos a muchos entre un empleado y un evento.
    """
    usuario = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    fecha_asistencia = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        ''' Obtener cadena representativa de nuestro usuario '''
        return f"{self.usuario.name} asiste al evento en {self.evento.lugar}"


class Viatico(models.Model):
    """
    Modelo que representa un Viatico en la BD
    """
    costo = models.FloatField()
    fecha_gasto = models.DateField()
    soporte = models.ImageField(upload_to='viaticos/')
    evento = models.ForeignKey('Evento', on_delete=models.CASCADE)
    tipo_viatico = models.ForeignKey(TipoViatico, on_delete=models.CASCADE)
    verificado = models.BooleanField()
    
    def __str__(self):
        return f"Viatico {self.id} en {self.evento}"