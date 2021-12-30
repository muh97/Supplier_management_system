from django.contrib import admin
from account.models import NewUser, Supplier, Hall, Comedy, Musician, Photographer, Party, Booking
from django.contrib.auth.admin import UserAdmin


# Register your models here.
class AdminSupplier(admin.ModelAdmin):
    list_display = ['id', 'user', 'company_name', 'type', 'deposit']


class AdminHall(admin.ModelAdmin):
    list_display = ['id', 'supplier', 'couples', 'cost_per_couple']


class AdminComedy(admin.ModelAdmin):
    list_display = ['id', 'supplier', 'charge_mile', 'price_small', 'price_wedding', 'price_hour']


class AdminParty(admin.ModelAdmin):
    list_display = ['id', 'supplier', 'charge_mile', 'price_small', 'price_wedding']


class AdminPhotographer(admin.ModelAdmin):
    list_display = ['id', 'supplier', 'charge_mile', 'price_small', 'price_wedding']


class AdminMusician(admin.ModelAdmin):
    list_display = ['id', 'supplier', 'tool', 'charge_mile', 'price_small', 'price_wedding']


class AdminBooking(admin.ModelAdmin):
    list_display = ['id', 'user', 'type','supplier','address','couple','couple_cost','deposit','total']


admin.site.register(NewUser)
admin.site.register(Supplier, AdminSupplier)
admin.site.register(Hall, AdminHall)
admin.site.register(Comedy, AdminComedy)
admin.site.register(Musician, AdminMusician)
admin.site.register(Photographer, AdminPhotographer)
admin.site.register(Party, AdminParty)
admin.site.register(Booking, AdminBooking)
