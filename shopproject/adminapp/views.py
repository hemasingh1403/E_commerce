from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from myapp.models import Category,Product,Customer
import os
# Create your views here.
def admin_login(request):
    if request.method=="POST":
        uname=request.POST.get('username')
        upass=request.POST.get('password')
        if uname=='admin' and upass=='12345':
            request.session['admin_id']=uname
            return redirect('dashboard/')
        else:
            return HttpResponse("Invalid username or Password!!!")
    return render(request,"admin/admin_login.html")



def addproduct_view(request):
    if request.session.get('admin_id'):
        if request.method=="POST":
            pname=request.POST.get('name')
            price=request.POST.get('price')
            cat=request.POST.get('category')
            des=request.POST.get('des')
            img=request.FILES['imag']
            cobj=Category.objects.get(id=cat)
            pobj=Product(name=pname,price=price,category=cobj,des=des,image=img)
            pobj.save()
            return redirect('viewproduct')
        cats=Category.objects.all()
        return render(request,"admin/addproduct.html",{'cats':cats})
    else:
        return redirect('/ adminuser/')  


def viewproduct_view(request):
    if request.session.get('admin_id'):
        prods=Product.objects.all()
        return render(request,'admin/viewproduct.html',{'prods':prods})
    else:
        return redirect('/adminuser/')  


def editproduct_view(request,id):
    if request.session.get('admin_id'):
        im=Product.objects.get(id=id)
        cats=Category.objects.all()    
        if request.method == "POST":
            img = im.image  # Start with the existing image

            # Check if a new image was uploaded
            if 'img' in request.FILES:
                new_img = request.FILES['img']
                
                # Remove old image file if it exists
                if im.image:
                    if os.path.isfile(im.image.path):
                        os.remove(im.image.path)
                
                img = new_img  # Assign new image
                            
            pname = request.POST.get('name')
            price = request.POST.get('price')
            cat = request.POST.get('category')
            des = request.POST.get('des')
            cobj=Category.objects.get(id=cat)
            pobj = Product.objects.get(id=id)
            pobj.name = pname
            pobj.price = price
            pobj.category = cobj
            pobj.des = des
            pobj.image = img
            pobj.save()
            return redirect('viewproduct')
        
        return render(request,"admin/editproduct.html",{'im':im ,'cats':cats})
    else:
        return redirect('/adminuser/')  


def deleteproduct_view(request,id):
    if request.session.get('admin_id'):
        rec=Product.objects.get(id=id)
        rec.delete()
        os.remove(rec.image.path)
        prods=Product.objects.all()
        return render(request,'admin/viewproduct.html',{'prods':prods})
    else:
        return redirect('/adminuser/')  

def deletecustomer_view(request,id):
    if request.session.get('admin_id'):
        rec=Customer.objects.get(id=id)
        rec.delete()
        os.remove(rec.img2.path)
        cust=Customer.objects.all()
        return render(request,'admin/viewcustomer.html',{'cust':cust})
    else:
        return redirect('/adminuser/')  

def deletecategory_view(request,id):
    if request.session.get('admin_id'):
        rec=Category.objects.get(id=id)
        rec.delete()
        os.remove(rec.img1.path)
        cats=Category.objects.all()
        return render(request,'admin/viewcategory.html',{'cats':cats})
    else:
        return redirect('/adminuser/')  

# @login_required('/login/')
def showproduct_view(request,id):
    if request.session.get('admin_id'):
        prods=Product.objects.get(id=id)
        return render(request,'admin/showproduct.html',{'prods':prods})
    else:
        return redirect('/adminuser/')  

def addcategory_view(request):
    if request.session.get('admin_id'):
        if request.method=="POST":
            cname=request.POST.get('name')
            des=request.POST.get('des')
            img=request.FILES.get('img')
            cobj=Category(name=cname,des=des,img1=img)
            cobj.save()
        return render(request,"admin/addcategory.html")
    else:
        return redirect('/adminuser/')  

def dashboard_view(request):
    if request.session.get('admin_id'):
        return render(request,"admin/dashboard.html")
    else:
        return redirect('/adminuser/')  

def viewcategory_view(request):
    if request.session.get('admin_id'):
        cats=Category.objects.all()
        return render(request,'admin/viewcategory.html',{'cats':cats})
    else:
        return redirect('/adminuser/')  

def viewcustomer_view(request):
    if request.session.get('admin_id'):
        cust=Customer.objects.all()
        return render(request,'admin/viewcustomer.html',{'cust':cust})
    else:
        return redirect('/adminuser/')  

def adminlogout_view(request):
    if request.session.get('admin_id'):            
        request.session.clear()
        return redirect('/adminuser/') 
    else:
        return redirect('/adminuser/')  