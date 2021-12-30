from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, AbstractUser
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator, ValidationError
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, redirect


# Create your models here.

class CustomAccountManager(BaseUserManager):

    def create_user(self, email, user_name, full_name, password, **other_fields):

        # other_fields.setdefault('is_active', True)
        if not email:
            raise ValueError('You must provide an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, user_name=user_name, full_name=full_name, is_active=True, **other_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, user_name, full_name, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_active', True)
        other_fields.setdefault('is_superuser', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('SuperUser must be assigned is_staff = True')

        if other_fields.get('is_superuser') is not True:
            raise ValueError('SuperUser must be assigned is_superuser = True')

        return self.create_user(email, user_name, full_name, password, **other_fields)


class NewUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    user_name = models.CharField(max_length=100, unique=True)
    full_name = models.CharField(max_length=150)
    address = models.TextField(blank=True)
    profile_img = models.ImageField(upload_to='profile', blank=True)
    phone = models.CharField(max_length=11)
    zipcode = models.CharField(max_length=5, blank=True)
    city = models.CharField(max_length=150, blank=True)
    country = models.CharField(max_length=150, blank=True)
    joined_date = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name', 'full_name', 'phone']

    def __str__(self):
        return self.user_name


class Supplier(models.Model):
    TYPE_CHOICES = (
        ('Hall', 'Hall'),
        ('Comedy', 'Comedy'),
        ('Photographer', 'Photographer'),
        ('Musician', 'Musician'),
        ('Party', 'Party'),
    )

    user = models.ForeignKey(NewUser, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=150)
    type = models.CharField(max_length=15, choices=TYPE_CHOICES)
    office_number = models.CharField(max_length=11, blank=True)
    company_email = models.EmailField(unique=True)
    zipcode = models.CharField(max_length=5)
    address = models.TextField()
    description = models.TextField(blank=True)
    deposit = models.PositiveSmallIntegerField(blank=True, verbose_name='Upfront Deposit')

    def __str__(self):
        return str(self.user)


class Hall(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='halls', blank=True)
    couples = models.PositiveSmallIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(120)],
                                               blank=True)
    cost_per_couple = models.PositiveSmallIntegerField(blank=True, verbose_name='cost/couple')

    def __str__(self):
        return str(self.supplier)

    def get_absolute_url(self):
        return redirect('hall')


class Comedy(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='comedy', blank=True)
    charge_mile = models.PositiveSmallIntegerField(verbose_name='charge/mile', blank=True)
    price_small = models.PositiveSmallIntegerField(verbose_name='price/small event', blank=True)
    price_wedding = models.PositiveSmallIntegerField(verbose_name='price/wedding', blank=True)
    price_hour = models.PositiveSmallIntegerField(verbose_name='price/hour', blank=True)

    def __str__(self):
        return str(self.supplier)


class Photographer(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='photographer', blank=True)
    charge_mile = models.PositiveSmallIntegerField(verbose_name='charge/mile', blank=True)
    price_small = models.PositiveSmallIntegerField(verbose_name='price/small event', blank=True)
    price_wedding = models.PositiveSmallIntegerField(verbose_name='price/wedding', blank=True)

    def __str__(self):
        return str(self.supplier)


class Party(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='party', blank=True)
    charge_mile = models.PositiveSmallIntegerField(verbose_name='charge/mile', blank=True)
    price_small = models.PositiveSmallIntegerField(verbose_name='price/small event', blank=True)
    price_wedding = models.PositiveSmallIntegerField(verbose_name='price/wedding', blank=True)

    def __str__(self):
        return str(self.supplier)


class Musician(models.Model):
    TYPE_CHOICES = (
        ('keyboard', 'keyboard'),
        ('singer', 'singer'),
        ('guitar', 'guitar'),
        ('saxophone', 'saxophone'),
        ('trumped', 'trumped'),
    )

    tool = models.CharField(max_length=15, choices=TYPE_CHOICES, blank=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='musician', blank=True)
    charge_lead = models.PositiveSmallIntegerField(verbose_name='charge/lead band', blank=True)
    band_arrange = models.PositiveSmallIntegerField(verbose_name='band arrangement cost', blank=True)
    price_man = models.PositiveSmallIntegerField(verbose_name='price/man', blank=True)
    price_small = models.PositiveSmallIntegerField(verbose_name='price/small', blank=True)
    price_wedding = models.PositiveSmallIntegerField(verbose_name='price/wedding', blank=True)
    charge_mile = models.PositiveSmallIntegerField(verbose_name='charge/mile', blank=True)

    def __str__(self):
        return str(self.supplier)


class Booking(models.Model):
    TYPE_CHOICES = (
        ('Small Event', 'Small Event'),
        ('Wedding', 'Wedding'),
        ('Family', 'Family'),
    )
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE)
    number = models.CharField(max_length=11, blank=True, verbose_name='contact no#')
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    type = models.CharField(max_length=15, choices=TYPE_CHOICES)
    category = models.CharField(max_length=15)
    couple = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(120)],
                                              blank=True, null=True)
    couple_cost = models.PositiveSmallIntegerField(blank=True, null=True)
    hour = models.PositiveSmallIntegerField(blank=True, null=True)
    hour_cost = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='hour cost')
    location = models.CharField(max_length=100, null=True, blank=True)
    distance_charges = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Distance Charges')
    event_cost = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name="Event Cost")
    wedding_cost = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Wedding Cost')
    band_arrange = models.BooleanField()
    charge_lead = models.BooleanField()
    man = models.PositiveSmallIntegerField(verbose_name='total gathering', blank=True, null=True)
    price_man = models.PositiveSmallIntegerField(verbose_name='price/man', blank=True, null=True)
    address = models.TextField()
    deposit = models.PositiveSmallIntegerField(blank=True, verbose_name='Upfront Deposit')
    total = models.PositiveSmallIntegerField(verbose_name='Total Cost', blank=True)
