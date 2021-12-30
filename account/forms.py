from django import forms
from account.models import NewUser, Supplier, Hall, Comedy, Photographer, Party, Musician, Booking
from django.contrib.auth.forms import UserCreationForm


class RegistrationForm(UserCreationForm):
    class Meta:
        model = NewUser
        fields = ('email', 'user_name', 'password1', 'password2',)


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        exclude = ('user',)


class HallForm(forms.ModelForm):
    prefix = 'hall'

    class Meta:
        model = Hall
        exclude = ('supplier',)


class ComedyForm(forms.ModelForm):
    prefix = 'comedy'

    class Meta:
        model = Comedy
        exclude = ('supplier',)


class PhotographerForm(forms.ModelForm):
    prefix = 'photographer'

    class Meta:
        model = Photographer
        exclude = ('supplier',)


class PartyForm(forms.ModelForm):
    prefix = 'party'

    class Meta:
        model = Party
        exclude = ('supplier',)


class MusicianForm(forms.ModelForm):
    prefix = 'music'

    class Meta:
        model = Musician
        exclude = ('supplier',)


class SupplierUpdateForm(forms.ModelForm):
    class Meta:
        model = Supplier
        exclude = ('user', 'type',)


class HallUpdateForm(forms.ModelForm):
    class Meta:
        model = Hall
        exclude = ('supplier',)


class ComedyUpdateForm(forms.ModelForm):
    class Meta:
        model = Comedy
        exclude = ('supplier',)


class PartyUpdateForm(forms.ModelForm):
    class Meta:
        model = Party
        exclude = ('supplier',)


class PhotographerUpdateForm(forms.ModelForm):
    class Meta:
        model = Photographer
        exclude = ('supplier',)


class MusicianUpdateForm(forms.ModelForm):
    class Meta:
        model = Musician
        exclude = ('supplier',)


class HallBooking(forms.ModelForm):
    # prefix = 'hall'

    class Meta:
        model = Booking
        exclude = ('user', 'category', 'hour', 'supplier',
                   'hour', 'hour_cost', 'location', 'distance_charges',
                   'event_cost', 'wedding_cost', 'band_arrange',
                   'charge_lead', 'man', 'price_man', 'total', 'couple_cost','deposit')


class ComedyBooking(forms.ModelForm):
    # prefix = 'comedy'
    LOCATION = (
        ('City', 'City'),
        ('Out of Station', 'Out of Station'),
    )
    location = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=LOCATION
    )

    class Meta:
        model = Booking
        exclude = ('user', 'category', 'couple', 'supplier',
                   'hour_cost', 'distance_charges',
                   'event_cost', 'wedding_cost', 'band_arrange',
                   'charge_lead', 'man', 'price_man', 'total', 'couple_cost','deposit'
                   )


class PartyBooking(forms.ModelForm):
    # prefix = 'booking'
    LOCATION = (
        ('City', 'City'),
        ('Out of Station', 'Out of Station'),
    )
    location = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=LOCATION
    )

    class Meta:
        model = Booking
        exclude = ('user', 'category', 'hour', 'couple', 'supplier',
                   'hour_cost', 'distance_charges', 'hour'
                                                    'event_cost', 'wedding_cost', 'band_arrange',
                   'charge_lead', 'man', 'price_man', 'total', 'couple_cost', 'event_cost','deposit')


class PhotographerBooking(forms.ModelForm):
    LOCATION = (
        ('City', 'City'),
        ('Out of Station', 'Out of Station'),
    )
    location = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=LOCATION
    )

    class Meta:
        model = Booking
        exclude = ('user', 'category', 'hour', 'couple', 'supplier',
                   'hour_cost', 'distance_charges', 'hour'
                                                    'event_cost', 'wedding_cost', 'band_arrange',
                   'charge_lead', 'man', 'price_man', 'total', 'couple_cost', 'event_cost','deposit')


class MusicianBooking(forms.ModelForm):
    # prefix = 'booking'
    LOCATION = (
        ('City', 'City'),
        ('Out of Station', 'Out of Station'),
    )
    location = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=LOCATION
    )

    class Meta:
        model = Booking
        exclude = ('user', 'category', 'hour', 'couple', 'supplier',
                   'hour_cost', 'distance_charges', 'hour'
                                                    'event_cost', 'wedding_cost',
                   'price_man', 'total', 'couple_cost', 'event_cost','deposit')
