from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import UserManager
from django.db import models


class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('User must have an email address')

        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(email, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=True)
    city = models.ForeignKey('scraping.City', on_delete=models.SET_NULL, null=True, blank=True)
    speciality = models.ForeignKey('scraping.Speciality', on_delete=models.SET_NULL, null=True, blank=True)
    send_email = models.BooleanField(default=True)
    objects = MyUserManager()
    USERNAME_FIELD = 'email'
    REQUAIRED_FIELDS = ['email']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
