from django.shortcuts import render,redirect
from .forms import UserAddForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User, Group
from .decorators import admin_only
from .models import StaffDetails,Pricing,GoodBooking,Reqpayment
from django.contrib.auth.decorators import login_required
from datetime import datetime

import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from django.http import HttpResponseBadRequest

razorpay_client = razorpay.Client(
  auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

@admin_only
def Index(request):
    price = Pricing.objects.all()
    context = {
        "price":price
    }
    return render(request,'index.html',context)

def SignIn(request):
    if request.method == "POST":
        username = request.POST['uname']
        password = request.POST['pswd']
        user1 = authenticate(request, username = username , password = password)
        
        if user1 is not None:
            
            request.session['username'] = username
            request.session['password'] = password
            login(request, user1)
            return redirect('Index')
        
        else:
            messages.info(request,'Username or Password Incorrect')
            return redirect('SignIn')
    return render(request,"login.html")


def SignUp(request):
    form = UserAddForm()
    if request.method == "POST":
        form = UserAddForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get("email")
            if User.objects.filter(username = username).exists():
                messages.info(request,"Username Exists")
                return redirect('SignUp')
            if User.objects.filter(email = email).exists():
                messages.info(request,"Email Exists")
                return redirect('SignUp')
            else:
                new_user = form.save()
                new_user.save()
                
                group = Group.objects.get(name='user')
                new_user.groups.add(group)
                
                messages.success(request,"User Created")
                return redirect('SignIn')
            
    return render(request,"register.html",{"form":form})

def SignOut(request):
    logout(request)
    return redirect('Index')

def ViewService(request,pk):
    price = Pricing.objects.get(id= pk)
    context = {
        "price":price
    }
    return render(request,'viewservice.html',context)

def CompanyHome(request):
    return render(request,"companyhome.html")

def AdminHome(request):
    user = request.user
    bookings = GoodBooking.objects.filter(staff_person = user.id)
    context = {
        "bookings":bookings
    }
    return render(request,"staffhome.html",context)


# staffffffff============================================================

def Staff(request):
    staffs  = StaffDetails.objects.all()
    form = UserAddForm()
    if request.method == "POST":
        form = UserAddForm(request.POST)
        cat = request.POST["cat"]
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get("email")
            if User.objects.filter(username = username).exists():
                messages.info(request,"Username Exists")
                return redirect('SignUp')
            if User.objects.filter(email = email).exists():
                messages.info(request,"Email Exists")
                return redirect('SignUp')
            else:
                new_user = form.save()
                new_user.save()
                
                group = Group.objects.get(name='staff')
                new_user.groups.add(group)
                
                staff = StaffDetails.objects.create(staffid = new_user,staffcat = cat)
                staff.save()
                
                messages.success(request,"Staff User Created")
                return redirect('Staff')
            
    context = {
        "form":form,
        "staffs":staffs
    }
    return render(request,"staffadd.html",context)

def DeleteStaff(request,pk):
    staff = StaffDetails.objects.get(id = pk)
    user = staff.staffid
    user.delete()
    messages.info(request,"Staff User Deleted")
    return redirect("Staff")
    
def PriceAdd(request):
    data = None
    if Pricing.objects.filter(user = request.user).exists():
        data = Pricing.objects.get(user = request.user)
        
    if request.method == "POST":
        cname = request.POST['cname']
        nprice = request.POST['nprice']
        exprice = request.POST['exprice']
        priprice = request.POST['priprice']
        img = request.FILES['img']
        
        if Pricing.objects.filter(user = request.user).exists():
            data = Pricing.objects.get(user = request.user)
            data.company_name = cname 
            data.image = img
            data.Normal_Amount = nprice
            data.Basic_Amount = exprice
            data.Paltinum_Amount = priprice
            data.save()
            messages.info(request,"Data Updated")
            return redirect("PriceAdd")
        else:
            price = Pricing.objects.create(company_name = cname,image = img, Normal_Amount = nprice, Basic_Amount = exprice, Paltinum_Amount= priprice,user= request.user)
            price.save()
            messages.info(request,'Data Added')
            return redirect("PriceAdd")
            
    context = {
        "data":data
    }
    return render(request,"price.html",context)

def Orders(request):
    user = request.user
    booking = GoodBooking.objects.filter(company = user.id)
    context = {
        "booking":booking
    }
    return render(request,"orders.html",context)

def OrderSigngleView(request,pk):
    order = GoodBooking.objects.get(id = pk)
    context = {
        "order":order
    }
    return render(request,"orderssignleview.html",context)

@login_required(login_url='SignIn')
def BookCargo(request,val):
    if request.method == "POST":
        name = request.POST["name"]
        address = request.POST["address"]
        dname = request.POST["dname"]
        phone = request.POST["phone"]
        email = request.POST["email"]
        house = request.POST["house"]
        city = request.POST["city"]
        state = request.POST["state"]
        country = request.POST["country"]
        itemtype = request.POST["itemtype"]
        weight = request.POST["weight"]
        
        booking = GoodBooking.objects.create(name = name,user = request.user,delivery_person_name = dname,d_House = house,d_City = city, d_state = state,d_country = country,d_phone = phone, d_email = email,from_address = address, weight = weight,itemtype = val, status = "item Ordered",company = val)
        booking.save()
        company = User.objects.get(id = int(val))
        price = Pricing.objects.get(user  = company)
        booking.total_amount = price.Normal_Amount 
        booking.save()
        
        messages.info(request,"Order Booked")
        return redirect('BookCargo',val = val)
    return render(request,"bookcargo.html")


@login_required(login_url='SignIn')
def BookCargo1(request,val):
    if request.method == "POST":
        name = request.POST["name"]
        address = request.POST["address"]
        dname = request.POST["dname"]
        phone = request.POST["phone"]
        email = request.POST["email"]
        house = request.POST["house"]
        city = request.POST["city"]
        state = request.POST["state"]
        country = request.POST["country"]
        itemtype = request.POST["itemtype"]
        weight = request.POST["weight"]
        
        booking = GoodBooking.objects.create(name = name,user = request.user,delivery_person_name = dname,d_House = house,d_City = city, d_state = state,d_country = country,d_phone = phone, d_email = email,from_address = address, weight = weight,itemtype = val, status = "item Ordered",company = val)
        booking.save()
        company = User.objects.get(id = int(val))
        price = Pricing.objects.get(user  = company)
        booking.total_amount = price.Basic_Amount 
        booking.save()
        messages.info(request,"Order Booked")
        return redirect('BookCargo',val = val)
    return render(request,"bookcargo.html")


@login_required(login_url='SignIn')
def BookCargo2(request,val):
    if request.method == "POST":
        name = request.POST["name"]
        address = request.POST["address"]
        dname = request.POST["dname"]
        phone = request.POST["phone"]
        email = request.POST["email"]
        house = request.POST["house"]
        city = request.POST["city"]
        state = request.POST["state"]
        country = request.POST["country"]
        itemtype = request.POST["itemtype"]
        weight = request.POST["weight"]
        
        booking = GoodBooking.objects.create(name = name,user = request.user,delivery_person_name = dname,d_House = house,d_City = city, d_state = state,d_country = country,d_phone = phone, d_email = email,from_address = address, weight = weight,itemtype = val, status = "item Ordered",company = val)
        booking.save()
        company = User.objects.get(id = int(val))
        price = Pricing.objects.get(user  = company)
        booking.total_amount = price.Paltinum_Amount 
        booking.save()
        
        messages.info(request,"Order Booked")
        return redirect('BookCargo',val = val)
    return render(request,"bookcargo.html")

@login_required(login_url='SignIn')
def Myorders(request):
    booking = GoodBooking.objects.filter(user = request.user)
    context = {
        "booking":booking
    }
    return render(request,'myorders.html',context)

@login_required(login_url='SignIn')
def DeleteOrder(request,pk):
    GoodBooking.objects.get(id = pk).delete()
    return redirect("Orders")

@login_required(login_url='SignIn')
def StaffAssign(request,pk):
    users = User.objects.all()
    staffitems = []
    for user in users:
        if user.groups.exists():
            if user.groups.all()[0].name == 'staff':
                staffitems.append(user)
                
    if request.method =="POST":
        booking = GoodBooking.objects.get(id = pk)
        staff = request.POST["staff"]
        booking.staff_person = staff
        booking.save()
        return redirect("OrderSigngleView",pk =pk)
    context = {
        "staffitems":staffitems
    }
    return render(request,"assignstaff.html",context)

@login_required(login_url='SignIn')
def Takeorder(request,pk):
    order = GoodBooking.objects.get(id = pk)
    if request.method == "POST":
        weight = request.POST["weight"]
        order.weight = weight
        order.order_taken = True 
        order.status = "Order Taken"
        order.pickup_date = datetime.now()
        order.trackid = str(order.pickup_date).format(order.id)
        order.total_amount = float(order.total_amount) * int(weight)
        order.save()
        return redirect('Takeorder',pk= pk)
        
    context = {
        "order":order
    }
    return render(request,"staffassignments.html",context)

@login_required(login_url='SignIn')
def Orderdespached(request,pk):
    book = GoodBooking.objects.get(id = pk)
    book.status = "Item Despached"
    book.save()
    return redirect("OrderSigngleView",pk = pk)
    

@login_required(login_url='SignIn')
def Orderdedelivered(request,pk):
    book = GoodBooking.objects.get(id = pk)
    book.status = "Item Delivered"
    book.deliverd_date = datetime.now()
    book.complation_status = True
    book.save()
    return redirect("OrderSigngleView",pk = pk)

@login_required(login_url='SignIn')
def Ordersignle(request,pk):
    order = GoodBooking.objects.get(id = pk)
    context = {
        "order":order
    }
    return render(request,"ordersingle.html",context)

@login_required(login_url='SignIn')
def paymentreq(request):
    payreq = Reqpayment.objects.filter(user = request.user)
    context = {
        "payreq":payreq
    }
    
    
    # context['amt'] = (product1.Product_price)*float(qty)

    return render(request,"paymentreq.html",context)

def makepaymet(request,pk):
    context = {}
    currency = 'INR'
    payreq  = Reqpayment.objects.get(id = pk)
    amount = payreq.booking.total_amount * 100 # Rs. 200
    

  # Create a Razorpay Order Pyament Integration.....
    razorpay_order = razorpay_client.order.create(dict(amount=amount,
                          currency=currency,
                          payment_capture='0'))

  # order id of newly created order.
    razorpay_order_id = razorpay_order["id"]
    callback_url = 'http://127.0.0.1:8000/makepaymet/paymenthandlercus'

  # we need to pass these details to frontend.
    
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url 
    context['slotid'] = "1",
    
    return render(request,"makepayment.html",context)



@login_required(login_url='SignIn')
def reqpayment(request,pk):
    order = GoodBooking.objects.get(id = pk)
    user  = order.user 
    pay = Reqpayment.objects.create(booking = order,user = user)
    pay.save()
    messages.info(request,"Payment Requested")
    return redirect("Takeorder",pk = pk)

@csrf_exempt
def paymenthandlercus(request):
    if request.method == "POST":
        try:
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }

      # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(params_dict)
            if result is not None:
                amount = 800 * 100 # Rs. 200
                try:
                    print("working 1")
                    razorpay_client.payment.capture(payment_id, amount)
                    return redirect('Success1')
          # render success page on successful caputre of payment
                except:
                    print("working 2")
                    return redirect('Success1')
                    
                    
          # if there is an error while capturing payment.
            else:
                return render(request, 'paymentfail.html')
        # if signature verification fails.    
        except:
            return HttpResponseBadRequest()
        
      # if we don't find the required parameters in POST data
    else:
  # if other than POST request is made.
        return HttpResponseBadRequest()
    
def Success1(request):
    return render(request,'Paymentconfirm.html')

def SearchByid(request):
    if request.method == "POST":
        trackid = request.POST["track"]
        if GoodBooking.objects.filter(trackid = trackid):
            product = GoodBooking.objects.get(trackid = trackid)
            return redirect('Ordersignle', pk = product.id)
            
        else:
            messages.info(request,"Track Not Found")
            return redirect('Index')
        
    return redirect("Index")
        
        
    
    
    
