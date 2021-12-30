from account.models import Supplier
from account.forms import (SupplierForm,HallForm,ComedyForm,
                           MusicianForm,PhotographerForm,PartyForm)

from django import template
register = template.Library()

@register.simple_tag
def form_type():
    sform = SupplierForm()
    form = ''
    if sform.is_valid():
        typ = sform.cleaned_data['type']

        if typ == 'Hall':
            form = HallForm()
        elif typ == 'Comedy':
            form = ComedyForm()
        elif typ == 'Photographer':
            form = PhotographerForm()
        elif typ == 'Party':
            form = PartyForm
        elif typ == 'Musician':
            form = MusicianForm()
        return form

@register.simple_tag(takes_context=True)
def form_type1(context, type):
    print(type)
    form = ''
    # value = request.GET.get('id_type')
    # if value == 'Hall':
    #     form = HallForm()
    # elif value == 'Comedy':
    #     form = ComedyForm()
    # elif value == 'Photographer':
    #     form = PhotographerForm()
    # elif value == 'Musician':
    #     form = MusicianForm()
    # elif value == 'PartyPlaner':
    #     form = PartyPlanerForm()
    return form


@register.simple_tag()
def form_type2(id_type):
    value = id_type
    form = ''
    if value == 'Hall':
        form = HallForm()
    elif value == 'Comedy':
        form = ComedyForm()
    elif value == 'Photographer':
        form = PhotographerForm()
    elif value == 'Musician':
        form = MusicianForm()
    elif value == 'Party':
        form = PartyForm()
    return form



