from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth.models import PermissionsMixin,AbstractBaseUser
from accounts.managers import CustomUserManager
from django.utils.translation import gettext_lazy as _
from multiselectfield import MultiSelectField
from django.db.models import Q


class CustomUser(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(_('email address main'), unique=True)
    name = models.CharField(max_length=255)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    # is_employee = models.BooleanField(default=True)
    # is_organization = models.BooleanField(default=False)

    class Types(models.TextChoices):
        ORGANIZATION = 'Organization',"ORGANIZATION"
        EMPLOYEE = 'Employee',"EMPLOYEE"

    default_type = Types.EMPLOYEE
    # type = models.CharField(_('Type'), max_length=255, choices=Types.choices, default=default_type)
    type = MultiSelectField(choices=Types.choices, default=[], null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        if not self.id:
            self.type = self.default_type
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.email


class EmployeeAdditional(models.Model):
    user = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
    address = models.CharField(max_length=1000)

    def __str__(self):
        return f"{self.user} - {self.address}"

class OrganizationAdditional(models.Model):
    user = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
    gst = models.CharField(max_length = 10)
    organization_location = models.CharField(max_length = 1000)

    def __str__(self):
        return f"{self.user} - {self.organization_location} - {self.gst}"

class OrganizationManager(models.Manager):
    def get_queryset(self,*args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(Q(type__contains = CustomUser.Types.ORGANIZATION))
        # return super().get_queryset(*args, **kwargs).filter(type = CustomUser.Types.ORGANIZATION)


class EmployeeManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(Q(type__contains = CustomUser.Types.EMPLOYEE))
        # return super().get_queryset(*args, **kwargs).filter(type = CustomUser.Types.EMPLOYEE)


# proxy model, it will not create a seperate table
class Organization(CustomUser):
    default_type = CustomUser.Types.ORGANIZATION
    objects = OrganizationManager()
    class Meta:
        proxy = True

    @property
    def showAdditional(self):
        return self.organizationadditional

class Employee(CustomUser):
    default_type = CustomUser.Types.EMPLOYEE
    objects = EmployeeManager()
    class Meta:
        proxy = True
    
    @property
    def showAdditional(self):
        return self.employeeadditional

