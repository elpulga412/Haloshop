from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db.models.fields import EmailField
from django.contrib.auth.models import Group
# Create your models here.

class MyUserManager(BaseUserManager):
    def create_user(self, email,full_name, phone=None, address=None, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            email=self.normalize_email(email),
            full_name=full_name,
            phone=phone,
            address=address,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_staffuser(self, email,full_name, phone, address, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            full_name=full_name,
            phone=phone,
            address=address,
        )
        user.is_active = True
        user.is_staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email,full_name, password):
        user = self.create_user(
            email=self.normalize_email(email),
            full_name=full_name,
            password=password,
        )
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        group, created = Group.objects.get_or_create(name="admin")
        user.groups.add(group)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=100, unique=True)
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=13, blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', ]

    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return self.is_superuser  # User nào được phép truy cập vào admin site

    def has_module_perms(self, add_label):
        return True
