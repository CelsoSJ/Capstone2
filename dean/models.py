from django.db import models
from django.contrib.auth.models import AbstractUser  #a class provided by django that serves as a base class for custom user models. It provides the foundation for creating a custom user model that extends Django's built-in user model
from django.contrib.auth.models import Permission  #allows us to use Django's built-in permission system, it also allows us to create custom permissions in addition to the default permissions


# Create your models here.

class Department(models.Model):
  name = models.CharField(max_length=4)

  def __str__(self):
    return self.name  #The __str__ function in Python is a special method that returns a string representation of an object.


class Role(models.Model):
  name = models.CharField(max_length=30)
  permissions = models.ManyToManyField(Permission)  # a role field which allows us to assign permissions to roles

  def __str__(self):
    return self.name


class Program(models.Model):
  name = models.CharField(max_length=5, null=True)
  department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)

  def __str__(self):
    return self.name


# creating a custom user with added fields
# add 'from django.contrib.auth.models import Abstractuser' at the top
class CustomUser(AbstractUser):
  address = models.CharField(max_length=255)
  birthday = models.DateField(null=True)
  middle_initial = models.CharField(max_length=1)
  role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)
  department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
  program = models.ForeignKey(Program, on_delete=models.SET_NULL, null=True)



