from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login_view'),
    path('logout', views.logout, name='logout'),
    path('register', views.register, name='register'),
    path('supplier', views.SupplierCreate.as_view(), name='supplier'),
    # path('supplier_detail/<int:pk>', views.SupplierDetail.as_view(), name='supplier_detail'),
    path('home', views.index, name='index'),
    path('supplier_info/',views.SupplierInf.as_view(), name='supplier_info'),
    # path('supplier_detail', views.SupplierDetail.as_view(), name='supplier_detail'),
    path('<str:user>/update-profile',views.UpdateSupplier.as_view(),name='update'),
    path('booking/<int:pk>',views.CreateBooking.as_view(),name='booking'),
    # path('hall',views.HallCreate.as_view(),name='hall'),
    # path('comedy',views.ComedyCreate.as_view(),name='comedy'),
    # path('photographer',views.PhotographerCreate.as_view(),name='photographer'),
    # path('party',views.PartyCreate.as_view(),name='party'),
    # path('musician',views.MusicianCreate.as_view(),name='musician'),
    # path('typechoose',views.TypeChoose,name='typechoose'),
    # path('supplier_info',views.SupplierInfo.as_view(),name='supplier_info'),
    # path('supplier_info/<str:ascend>',views.SupplierInf.as_view(),name='supplier_inf'),


]