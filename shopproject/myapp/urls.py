from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('about/',views.about,name='about'),
    path('contact/',views.contact,name='contact'),
    
    path('user/viewproduct/',views.viewproduct.as_view(),name='user/viewproduct'),
    path('login/',views.login,name='login'),
    path('singup/',views.singup,name='singup'),
    path('logout/',views.logout_view,name='logout'),  
    path('cart/',views.cart_view,name='cart'),
    path('cong/',views.cong,name='cong'),
    path('profile/',views.profile,name='profile'),
    path('editcustomer/',views.editcustomer_view,name='editcustomer'),
    path('changepass/',views.changepass_view,name='changepass'),
    path('forgetpass/',views.forgetpassword_view,name='forgetpass'),
    path('otp/',views.otp_view,name="otp"),
    path('forgetchange/',views.forgetchange_view,name='forgetchange'),
]

