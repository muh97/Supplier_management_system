from django.shortcuts import render, redirect, reverse, get_object_or_404
from account.forms import RegistrationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import auth
from django.contrib.admin.forms import AuthenticationForm
from django.views.generic import (ListView, View)
from account.models import (Supplier, Hall, Comedy,
                            Photographer, Party, Musician, NewUser)
from account.forms import (SupplierForm, HallForm, ComedyForm,
                           MusicianForm, PhotographerForm, PartyForm)
from account.forms import (SupplierUpdateForm, HallUpdateForm, ComedyUpdateForm,
                           PartyUpdateForm, MusicianUpdateForm, PhotographerUpdateForm)
from account.forms import (HallBooking, ComedyBooking, PartyBooking,
                           PhotographerBooking, MusicianBooking)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Q


# Create your views here.

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if Supplier.objects.filter(user=user):
                return redirect('supplier_info')
            else:
                return redirect('index')
    else:
        form = AuthenticationForm(request.POST)
    return render(request, 'login.html', {'form': form})


def register(request):
    form = RegistrationForm()
    if request.POST:
        form1 = RegistrationForm(request.POST)
        if form1.is_valid():
            user = form1.save()
            login(request, user)
            return redirect('login_view')
    else:
        form = RegistrationForm(request.POST)
    return render(request, 'register.html', {'form': form})


@login_required(login_url='login_view')
def logout(request):
    auth.logout(request)
    return redirect('login_view')


@login_required(login_url='login_view')
def index(request):
    user = request.user
    supplier = Supplier.objects.filter(user=user)
    return render(request, 'index.html', {'supplier': supplier})


class SupplierCreate(LoginRequiredMixin, View):
    template_name = 'supplier.html'
    login_url = 'login_view'

    def get(self, request, *args, **kwargs):
        sform = SupplierForm
        hform = HallForm(prefix='hall')
        cform = ComedyForm(prefix='comedy')
        mform = MusicianForm(prefix='music')
        pform = PhotographerForm(prefix='photographer')
        kform = PartyForm(prefix='party')
        return render(request, self.template_name, {'sform': sform, 'hform': hform, 'cform': cform,
                                                    'mform': mform, 'pform': pform, 'kform': kform})

    def post(self, request, *args, **kwargs):
        hform = HallForm(prefix='hall')
        cform = ComedyForm(prefix='comedy')
        mform = MusicianForm(prefix='music')
        pform = PhotographerForm(prefix='photographer')
        kform = PartyForm(prefix='party')
        sform = SupplierForm(request.POST, request.FILES)
        typ = request.POST.get('type')

        forms = {'Hall': HallForm(request.POST, request.FILES), 'Comedy': ComedyForm(request.POST, request.FILES),
                 'Musician': MusicianForm(request.POST, request.FILES),
                 'Photographer': PhotographerForm(request.POST, request.FILES),
                 'Party': PartyForm(request.POST, request.FILES)}

        form = forms.get(typ)

        if sform.is_valid() and form.is_valid():
            sform = sform.save(commit=False)
            sform.user = request.user
            sform.save()
            form = form.save(commit=False)
            form.supplier = sform
            form.save()
            return redirect('supplier')

        form_dict = {typ: form}
        context = {
            'sform': sform,
            'hform': form_dict.get('Hall', hform),
            'cform': form_dict.get('Comedy', cform),
            'pform': form_dict.get('Musician', pform),
            'kform': form_dict.get('Photographer', kform),
            'mform': form_dict.get('Party', mform),
        }
        return render(request, self.template_name, context)

    def get_success_url(self):
        return reverse('supplier')


class SupplierInf(LoginRequiredMixin, ListView):
    template_name = 'supplier_info.html'
    login_url = 'login_view'
    model = Supplier

    def get_queryset(self, *args, **kwargs):
        supp = self.request.GET.get('supplier')
        ab = self.request.GET.get('type')
        mini = self.request.GET.get('min_deposit')
        maxi = self.request.GET.get('max_deposit')

        if self.request.GET.get('supplier') and self.request.GET.get('type') \
                and self.request.GET.get('min_deposit') and self.request.GET.get('max_deposit'):
            qs = Supplier.objects.filter(Q(user__full_name__icontains=supp), Q(type__icontains=ab),
                                         Q(deposit__gt=mini, deposit__lt=maxi))

        elif self.request.GET.get('supplier') and self.request.GET.get('type'):
            qs = Supplier.objects.filter(Q(user__full_name__icontains=supp) & Q(type__icontains=ab))

        elif self.request.GET.get('supplier') and self.request.GET.get('min_deposit') \
                and self.request.GET.get('max_deposit'):
            qs = Supplier.objects.filter(Q(user__full_name__icontains=supp) & Q(deposit__gt=mini, deposit__lt=maxi))

        elif self.request.GET.get('type') and self.request.GET.get('min_deposit') \
                and self.request.GET.get('max_deposit'):
            qs = Supplier.objects.filter(Q(type__icontains=ab) & Q(deposit__gt=mini, deposit__lt=maxi))

        elif self.request.GET.get('supplier'):
            qs = Supplier.objects.filter(user__full_name__icontains=supp)

        elif self.request.GET.get('type'):
            qs = Supplier.objects.filter(type__icontains=ab)

        elif self.request.GET.get('min_deposit') and self.request.GET.get('max_deposit'):
            qs = Supplier.objects.filter(deposit__gt=mini, deposit__lt=maxi)

        else:
            qs = Supplier.objects.all()

        if 'ascend' in self.request.GET:
            qs = qs.order_by('deposit')
            return qs
        elif 'descend' in self.request.GET:
            qs = qs.order_by('-deposit')
            return qs
        else:
            return qs


class SupplierDetail(LoginRequiredMixin, ListView):
    template_name = 'supplier_detail.html'
    login_url = 'login_view'
    model = Supplier

    def get_queryset(self):
        user = self.request.user
        ab = self.request.GET.get('type')
        mini = self.request.GET.get('min_deposit')
        maxi = self.request.GET.get('max_deposit')

        if self.request.GET.get('type') and self.request.GET.get('min_deposit') \
                and self.request.GET.get('max_deposit'):
            qs = Supplier.objects.filter(Q(type__icontains=ab), Q(deposit__gt=mini, deposit__lt=maxi)
                                         & Q(user=user))

        elif self.request.GET.get('type'):
            qs = Supplier.objects.filter(Q(type__icontains=ab) & Q(user=user))

        elif self.request.GET.get('min_deposit') and self.request.GET.get('max_deposit'):
            qs = Supplier.objects.filter(Q(user=user) & Q(deposit__gt=mini, deposit__lt=maxi))

        else:
            qs = Supplier.objects.filter(user=user)

        if 'ascend' in self.request.GET:
            qs = qs.order_by('deposit')
            return qs
        elif 'descend' in self.request.GET:
            qs = qs.order_by('-deposit')
            return qs
        else:
            return qs


def mode(typ):
    mod = {'Hall': Hall,
           'Comedy': Comedy,
           'Musician': Musician,
           'Photographer': Photographer,
           'Party': Party,
           }
    return mod.get(typ)


def forms(typ):
    form = {'Hall': HallUpdateForm,
            'Comedy': ComedyUpdateForm,
            'Musician': MusicianUpdateForm,
            'Photographer': PhotographerUpdateForm,
            'Party': PartyUpdateForm
            }
    return form.get(typ)


class UpdateSupplier(LoginRequiredMixin, View):
    login_url = 'login_view'
    template_name = 'update_supplier.html'

    def get(self, request, *args, **kwargs):
        supplier = get_object_or_404(Supplier, user=request.user)
        suform = SupplierUpdateForm(instance=supplier)
        typ = supplier.type
        form1 = mode(typ)
        form = forms(typ)
        form2 = form(instance=get_object_or_404(form1, supplier__user=request.user))

        context = {
            'suform': suform,
            'form': form2,
            'supplier': supplier,
        }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        supplier = get_object_or_404(Supplier, user=request.user)
        suform = SupplierUpdateForm(request.POST, request.FILES, instance=supplier)
        typ = supplier.type
        form1 = mode(typ)
        form2 = forms(typ)
        form = form2(request.POST, request.FILES, instance=get_object_or_404(form1, supplier__user=request.user))

        if suform.is_valid() and form.is_valid():
            suform.save()
            form.save()
            return redirect('supplier_info')

        context = {
            'suform': suform,
            'form': form,
        }

        return render(request, self.template_name, context)


def booking_form(typ):
    form = {'Hall': HallBooking,
            'Comedy': ComedyBooking,
            'Party': PartyBooking,
            'Photographer': PhotographerBooking,
            'Musician': MusicianBooking,
            }

    return form.get(typ)


class CreateBooking(View):
    login_url = 'login_view'
    template_name = 'booking.html'

    def get(self, request, pk, *args, **kwargs, ):
        data = Supplier.objects.get(id=pk)
        typ = data.type
        form = booking_form(typ)

        context = {
            'form': form,
        }
        return render(request, self.template_name, context)

    def post(self, request, pk, *args, **kwargs):
        data = Supplier.objects.get(id=pk)
        typ = data.type
        form1 = booking_form(typ)
        form = form1(request.POST)

        if form.is_valid():
            form = form.save(commit=False)
            form.supplier = data
            form.user = request.user
            form.category = typ

            if typ == "Hall":
                hall_data = Hall.objects.get(supplier=data)
                form.couple = int(request.POST.get('couple'))
                form.couple_cost = hall_data.cost_per_couple * form.couple
                form.deposit = data.deposit
                form.total = form.couple_cost - form.deposit
                form.save()

            elif typ == "Comedy":
                comedy_data = Comedy.objects.get(supplier=data)


        else:
            form = form
        context = {
            'form': form,
        }

        return render(request, self.template_name, context)
