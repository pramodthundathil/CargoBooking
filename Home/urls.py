from django.urls import path 
from .import views 

urlpatterns = [
    path("",views.Index,name="Index"),
    path("SignOut",views.SignOut,name="SignOut"),
    path("SignIn",views.SignIn,name="SignIn"),
    path("SignUp",views.SignUp,name="SignUp"),
    path("ViewService/<int:pk>",views.ViewService,name="ViewService"),
    path("CompanyHome",views.CompanyHome,name="CompanyHome"),
    path("Staff",views.Staff,name="Staff"),
    path("DeleteStaff/<int:pk>",views.DeleteStaff,name="DeleteStaff"),
    path("PriceAdd",views.PriceAdd,name="PriceAdd"),
    path("Orders",views.Orders,name="Orders"),
    path("BookCargo/<str:val>",views.BookCargo,name="BookCargo"),
    path("BookCargo1/<str:val>",views.BookCargo1,name="BookCargo1"),
    path("BookCargo2/<str:val>",views.BookCargo1,name="BookCargo2"),
    path('Myorders',views.Myorders,name="Myorders"),
    path('AdminHome',views.AdminHome,name="AdminHome"),
    path("OrderSigngleView/<int:pk>",views.OrderSigngleView,name="OrderSigngleView"),
    path("DeleteOrder/<int:pk>",views.DeleteOrder,name="DeleteOrder"),
    path("StaffAssign/<int:pk>",views.StaffAssign,name="StaffAssign"),
    path("Takeorder/<int:pk>",views.Takeorder,name="Takeorder"),
    path("Orderdespached/<int:pk>",views.Orderdespached,name="Orderdespached"),
    path("Orderdedelivered/<int:pk>",views.Orderdedelivered,name="Orderdedelivered"),
    path("Ordersignle/<int:pk>",views.Ordersignle,name="Ordersignle"),
    path("reqpayment/<int:pk>",views.reqpayment,name="reqpayment"),
    path("paymentreq",views.paymentreq,name="paymentreq"),
    path("/makepaymet/paymenthandlercus",views.paymenthandlercus,name="paymenthandlercus"),
    path("makepaymet/<int:pk>",views.makepaymet,name="makepaymet"),
    path("SearchByid",views.SearchByid,name="SearchByid")
]

