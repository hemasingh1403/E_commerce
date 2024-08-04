from django.urls import path
from .import views



urlpatterns = [
    path('',views.admin_login,name='adminlogin'),
    path('adminlogout/',views.adminlogout_view,name='adminlogout'),
    path('dashboard/',views.dashboard_view,name='dashboard'),
    path('addproduct/',views.addproduct_view,name='addproduct'),
    path('viewproduct/',views.viewproduct_view,name='viewproduct'),
    path('deleteproduct/<int:id>/',views.deleteproduct_view,name='deleteproduct'),
    path('deletecustomer/<int:id>/',views.deletecustomer_view,name='deletecustomer'),
    path('deletecategory/<int:id>/',views.deletecategory_view,name='deletecategory'),
    path('editproduct/<int:id>/',views.editproduct_view,name='editproduct'),
    path('showproduct/<int:id>/',views.showproduct_view,name='showproduct'),
    path('addcategory/',views.addcategory_view,name='addcategory'),
    path('viewcategory/',views.viewcategory_view,name='viewcategory'),
    path('viewcustomer/',views.viewcustomer_view,name='viewcustomer'),
    
]
