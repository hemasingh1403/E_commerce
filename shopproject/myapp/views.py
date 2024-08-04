from django.shortcuts import render, redirect, HttpResponse
from django.http import HttpResponse
import os
#from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from .models import Category,Product,Customer,cart
from django.views import View
#send mail
from django.core.mail import send_mail , EmailMessage
from django.conf import settings
import random
import datetime
from django.utils import timezone
def index(request):
    if request.method == "POST":
        # Retrieve the current cart from session or initialize an empty dictionary
        pcart = request.session.get('cart', {})
        
        # Retrieve product ID, remove flag, and category ID from POST request
        pid = request.POST.get('addproduct')
        rm = request.POST.get('remove')
        cid = request.POST.get('cid')
        
        # Debug prints (optional)
        print(pid, '==============================================================')
        print(rm, '================================================================')
        
        if pcart:
            # Retrieve current quantity of the product in cart
            qty = pcart.get(pid)
            
            if qty:
                if rm:
                    # If 'remove' flag is set, decrease quantity or remove if <= 1
                    if qty <= 1:
                        pcart.pop(pid)
                    else:
                        qty -= 1
                        pcart[pid] = qty
                else:
                    # Otherwise, increase quantity
                    qty += 1
                    pcart[pid] = qty
            else:
                # If product not in cart, add it with quantity 1
                pcart[pid] = 1
        else:
            # If cart is empty, add the product with quantity 1
            pcart[pid] = 1
        
        # Update the session with the modified cart
        request.session['cart'] = pcart
        
        # Debug print to check updated cart (optional)
        print(request.session.get('cart'))
        return redirect('/')
    
    # Fetch all categories and products if request method is not POST
    cats = Category.objects.all()
    prods = Product.objects.all()
    
    # Render the index.html template with categories and products
    return render(request, "user/index.html", {'cats': cats, 'prods': prods})



def about(request):
    return render(request,"user/about.html")
def contact(request):
    return render(request,"user/contact.html")


class viewproduct(View):
    def post(self,request):
        pcart=request.session.get('cart',{})
        pid=request.POST.get('addproduct')
        rm=request.POST.get('remove')
        cid = request.POST.get('cid')
        print(pid,'==============================================================')
        print(rm,'================================================================')
        if pcart:
            qty=pcart.get(pid)
            if qty:
                    if rm:
                        if qty<=1:
                            pcart.pop(pid)
                        else:
                            qty=qty-1
                            pcart[pid]=qty    
                    else:
                        qty=qty+1
                        pcart[pid]=qty
            else:
                pcart[pid]=1    
        else:
            pcart[pid]=1
        request.session['cart']=pcart
        print(request.session.get('cart'))
        if cid:
           prods=Product.objects.filter(category=cid) 
        return render(request,"user/viewproduct.html",{'prods':prods,'cid':cid})

    def get(self,request):
        cid=request.GET.get('category')
        if cid:
           prods=Product.objects.filter(category=cid) 
        return render(request,"user/viewproduct.html",{'prods':prods,'cid':cid})


def login(request):
    if request.method=="POST":
        uname=request.POST.get('email')
        upass=request.POST.get('password')
        cust1=Customer.objects.filter(email=uname)
        print('hello',uname,upass)
        print(cust1) 
        print("hello2")
        for cust in cust1:
            if str(uname)==cust.email and str(upass)==cust.pass1:
                request.session['cust_id']=cust.id
                request.session['cust_name']=cust.fname
                request.session['cust_email']=cust.email
                return redirect('index')
            else:
                return HttpResponse("user did not match")
    return render(request,"user/login.html") 

def logout_view(request):
    if request.session.get('cust_id'):
            
        request.session.clear()
        return redirect('/')
    else:
        return redirect('login')      

def singup(request):
    if request.method=="POST":
        fname=request.POST.get('fname')
        lname=request.POST.get('lname')
        father=request.POST.get('father')
        email=request.POST.get('email')
        pass1=request.POST.get('password')
        pass2=request.POST.get('cpassword')
        phone=request.POST.get('phone')
        ad=request.POST.get('address')
        img=request.FILES.get('img')
        if pass1==pass2:
            cobj=Customer(fname=fname,lname=lname,father=father,email=email,pass1=pass1,Phone=phone,address=ad,img2=img)
            #cobj.pass1=make_password(cobj.pass1)
            cobj.save()
            return redirect('/login/')
        else:
            return HttpResponse("Password did not match")
    return render(request,"user/singup.html") 


def cart_view(request):
    if request.session.get('cust_id'):
        c="true"
        request.session['cong']=c

        ids=[]
        try:
            ids=list(request.session.get('cart').keys())
        except:
            pass    
        prods=Product.objects.filter(id__in=ids)
        return render(request,"user/cart.html",{'prods':prods}) 
    else:
        return redirect('login')  

def profile(request):
    if request.session.get('cust_id'):
        cst_id=request.session.get('cust_id')
        if cst_id:
            cust=Customer.objects.get(id=cst_id)
            return render(request,"user/profile.html",{'cust':cust})
    else:
        return redirect('login')  

def editcustomer_view(request):
    if request.session.get('cust_id'):
        cst_id=request.session.get('cust_id')
        cust=Customer.objects.get(id=cst_id)
        

        if request.method=="POST":
            print("=========")
            img = cust.img2  # Start with the existing image

            # Check if a new image was uploaded
            if 'img' in request.FILES:
                new_img = request.FILES['img']
                print("111111111111")
                
                # Remove old image file if it exists
                if cust.img2:
                    print("22222222222222")
                    if os.path.isfile(cust.img2.path):
                        os.remove(cust.img2.path)
                
                img = new_img  # Assign new image
                            
            fname=request.POST.get('fname')
            lname=request.POST.get('lname')
            father=request.POST.get('father')
            email=request.POST.get('email')
            phone=request.POST.get('phone')
            ad=request.POST.get('address')
            print(fname,"========",father)
            cobj=Customer.objects.get(id=cst_id)
            cobj.fname = fname
            cobj.lname = lname
            cobj.father = father
            cobj.email = email
            cobj.Phone = phone
            cobj.address = ad
            cobj.img2 = img
            cobj.pass1 = cobj.pass1
            cobj.save()
            return redirect('profile')
        return render(request,"user/editcustomer.html",{'cust':cust})
    else:
        return redirect('login')

def changepass_view(request):
    if request.session.get('cust_id'):
        if request.method == "POST":
            cust_id = request.session.get('cust_id')
            if cust_id:
                cust = Customer.objects.get(id=cust_id)
                old_password = request.POST.get('old_pass')
                print(type(old_password),old_password)
                print(type(cust.pass1),cust.pass1)
                if cust.pass1 == old_password:
                    new_password = request.POST.get('new_pass')
                    confirm_new_password = request.POST.get('confirm_newpass')
                    print(new_password,confirm_new_password)
                    if new_password == confirm_new_password:
                        # Update the customer's password
                        obj=Customer(id=cust.id,fname=cust.fname,lname=cust.lname,father=cust.father,email=cust.email,address=cust.address,Phone=cust.Phone,img2=cust.img2,pass1=new_password)
                        obj.save()
                        return redirect('/')
                    else:
                        return HttpResponse("New passwords do not match.")
                else:
                    return HttpResponse("Invalid old password.")
        return render(request, "user/changepass.html")
    else:
        return redirect('login')


def forgetpassword_view(request):
    if request.session.get('cust_id'):
        if request.method == "POST":
            email = request.POST.get('email')
            try:
                cust = Customer.objects.get(email=email)
            except Customer.DoesNotExist:
                return HttpResponse("Invalid email")

            # Generate OTP
            rm = random.randint(135267, 987654)
            expiry_time = datetime.datetime.now() + datetime.timedelta(seconds=60)  # Set expiry time to 30 seconds from now

            # Store OTP and email in session with expiry time
            request.session['otp_id'] = rm
            request.session['expiry_time'] = expiry_time.strftime('%Y-%m-%d %H:%M:%S')  # Convert datetime to string

            request.session['email_for_reset'] = email

            subject = 'Password Reset OTP'
            message = f"Your OTP for password reset is {rm}. Please use it within 60 seconds."
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [email]

            try:
                send_mail(subject, message, from_email, recipient_list)
            except Exception as e:
                return HttpResponse("Failed to send OTP. Please try again later.")
            return redirect('otp')  # Redirect to OTP verification page

        return render(request, "user/forgetpass.html")
    else:
        return redirect('login')


def otp_view(request):
    if request.session.get('cust_id'):
        if request.session.get('otp_id'):    
            if request.method == "POST":
                sotp = request.session.get('otp_id')
                uotp = request.POST.get('user_otp')
                print(sotp,'===',uotp)

                if str(sotp) == uotp:
                    # Check if OTP is within the 60-second window
                    expiry_time_str = request.session.get('expiry_time')
                        
                    try:
                        expiry_time = datetime.datetime.strptime(expiry_time_str, '%Y-%m-%d %H:%M:%S')
                    except ValueError:
                        return HttpResponse("Invalid expiry time format in session. Cannot validate OTP.")

                    current_time = datetime.datetime.now()
                        
                    if current_time <= expiry_time:
                        # If current time is less than or equal to expiry time, redirect to password change page
                        request.session['otp_verified'] = True
                        return redirect('forgetchange')  # Replace 'forgetchange' with your actual password change URL name
                    
                    else:
                        return HttpResponse("OTP has expired. Please request a new one.")
                else:
                    return HttpResponse("Invalid OTP. Please try again.")

            return render(request, "user/otp.html")
        else:
            return redirect('forgetpass')
    else:
        return redirect('login')
    

def forgetchange_view(request):
    if request.session.get('cust_id'):
        if request.session.get('otp_verified'):
            if request.method == "POST":
                cust_id = request.session.get('cust_id')
                if cust_id:
                    cust = Customer.objects.get(id=cust_id)
                    new_password = request.POST.get('new_pass')
                    confirm_new_password = request.POST.get('confirm_newpass')
                    print(new_password,confirm_new_password)
                    if new_password == confirm_new_password:
                        # Update the customer's password
                        print("22222222222222")
                        obj=Customer(id=cust.id,fname=cust.fname,lname=cust.lname,father=cust.father,email=cust.email,address=cust.address,Phone=cust.Phone,img2=cust.img2,pass1=new_password)
                        obj.save()
                        return redirect('profile')
                    else:
                            return HttpResponse("New passwords do not match.")
                else:
                    return HttpResponse("Invalid old password.")
                    
            return render(request, "user/forgetchange.html")
        else:
            return redirect('otp')
    else:
        return redirect('login')    
    
def cong(request):
    if request.session.get('cust_id'):
        if request.session.get('cong'):
            return render(request, "user/congratulation.html")
        else:
            return render(request,"user/cart.html")
    else:
        return redirect('login') 

