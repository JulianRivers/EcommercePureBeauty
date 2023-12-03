from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, BaseUserManager)
from django.contrib.auth.models import AbstractUser

# Modelos de la base de datos relacionados a los usuarios clientes o administrador


class Pais (models.Model):
    """
    Modelo que representa la tabla en la BD de Paises
    """
    nombre = models.CharField('Nombre', max_length=100)

    def __str__(self):
        """
        Representación en un String del departamento
        """
        return f"País: {self.nombre}"


class Departamento (models.Model):
    '''Modelo que representa la tabla en la BD de Departamentos'''

    nombre = models.CharField('Nombre', max_length=100)
    departamento = models.ForeignKey(Pais, on_delete=models.CASCADE)

    def __str__(self):
        '''Representación en un String del departamento'''

        return f"Departamento: {self.nombre}"


class Ciudad (models.Model):
    '''Modelo que representa la tabla en la BD de Ciudades/Municipios'''

    nombre = models.CharField('Nombre', max_length=100)
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE)

    def __str__(self):
        '''Representación en un String de la ciudad'''
        return f"Ciudad: {self.nombre}"


class UserProfileManager(BaseUserManager):
    """ Manager del Modelo de Perfil de Usarios """

    def create_user(self, email, name, apellidos, password=None):
        """ Crear nuevo UserProfile"""
        if not email:
            raise ValueError('Usuario debe tener un email')

        email = self.normalize_email(email)
        user = self.model(email=email, name=name, apellidos=apellidos)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, apellidos, password):
        """ Crear un Super Usuario"""
        user = self.create_user(email, name, apellidos, password)
        user.is_superuser = True
        user.is_staff = True

        user.save(using=self._db)

        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """ Modelo Base de datos para Usuarios en el Sistema """
    email = models.EmailField('Email', max_length=255, unique=True)
    name = models.CharField('Nombres', max_length=100)
    apellidos = models.CharField('Apellidos', max_length=100)
    direccion = models.CharField('Direccion', max_length=500)
    celular = models.CharField('Celular', max_length=20, null=True)
    ciudad = models.ForeignKey(Ciudad, on_delete=models.CASCADE, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)

    class Meta:
        swappable = 'AUTH_USER_MODEL'

    class Meta(AbstractUser.Meta):
        pass

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
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


class Carrito (models.Model):
    '''Modelo que representa la tabla en la BD de los Carritos de compras'''
    usuario = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField('Fecha de creación')

    def __str__(self):
        '''Representación en un String del carrito de compras'''
        return f"Carrito de {self.usuario.name}"
