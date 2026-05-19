from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib import messages
from .models import *
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
# Create your views here.

def index(request):
    pro = Product.objects.all()[:8]  # Get first 8 products for display
    return render(request, 'index.html', {'products': pro})

def search(request):
    if request.method == 'POST':
        search = request.POST['search'] 
        pro=Product.objects.filter(Q(pname__icontains = search) | Q(pdis__icontains = search) )
        if not pro:
            messages.error(request, 'No product found')
            return redirect('/shop/')
        else:
            return render(request,'search.html',{'pro':pro})
    return render(request,'/shop.html')

def shop(request):
    pro=Product.objects.all()
    pagi=Paginator(pro,2)
    page_number=request.GET.get('page')
    final_page=pagi.get_page(page_number)
    return render(request, 'shop.html', {'final_page':final_page,'page_number':page_number})

def detail(request, id):
    product = Product.objects.get(pid=id)
    return render(request, 'detail.html', {'product': product})

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        # Save contact message to database
        contact_msg = Contact(
            name=name,
            email=email,
            subject=subject,
            message=message
        )
        contact_msg.save()
        
        messages.success(request, 'Thank you for contacting us! We will get back to you soon.')
        return redirect('/contact/')
    
    return render(request, 'contact.html')

def register(request):
    if request.method == 'POST':
        fn=request.POST["fname"]
        ln=request.POST["lname"]
        un=request.POST["uid"]
        em=request.POST["email"]
        pass1=request.POST["pass1"]
        pass2=request.POST["pass2"]
    
        if pass1==pass2:
            if User.objects.filter(username=un).exists():
                messages.success(request,"You already have")
                return redirect('/register/')
            elif User.objects.filter(email=em).exists():
                messages.error(request,"Email already registered")
                return redirect('/register/')
            else:
                u=User.objects.create_user(first_name=fn,last_name=ln,username=un, email=em, password=pass1)
                u.save()
                messages.success(request,"Registration successful")
                return redirect( '/')   
        else:
            messages.error(request,"Passwords don't match")
            return redirect('/register/') 
    return render(request, 'register.html')

def login(request):
    if request.method == 'POST':
        un=request.POST["uid"]
        psw=request.POST["pass1"]

        user=auth.authenticate(username=un, password=psw)
        if user is not None:
            auth.login(request ,user)
            messages.success(request,"login successful")
            return redirect('/')
        else:
            messages.error(request,"uname or password mismatch")
            return redirect('/login/')
    return render(request,'login.html')

def logout(request):
    auth.logout(request)
    messages.success(request,'logout successful')
    return redirect('/')


def category(request,id):
    data = Product.objects.filter(c_id=id)
    cdata=Category.objects.filter(cid=id)
    
    # cname=cdata.cname
    return render(request, 'category.html', {'data': data,'cdata':cdata})


@login_required(login_url='/login/')
def cart(request):
    cart_data=Cart.objects.filter(u_id=request.user)
    subtotal = sum(item.sub_total() for item in cart_data)
    shipping = 50  # Fixed shipping charge
    total = subtotal + shipping
    return render(request, 'cart.html',{'cart_data': cart_data, 'subtotal': subtotal, 'shipping': shipping, 'total': total})




@login_required(login_url='/login/')
def addtocart(request, id):
    try:
        p = Product.objects.get(pid=id)
    except Product.DoesNotExist:
        messages.error(request, 'Product does not exist!')
        return redirect('/shop/')

    # Check if the product is already in the cart
    data = Cart.objects.filter(u_id=request.user, p_id=id)
    if data:
        messages.warning(request, 'Product is already in the cart!!')
        w_data = Wishlist.objects.filter(u_id=request.user, p_id=id)
        if w_data.exists():
            w_data.delete()
        return redirect('/cart/')
    else:
        # Add product to the cart
        s = Cart(p_id=p, u_id=request.user, quantity=1)
        s.save()

        # Remove the product from the wishlist
        w_data = Wishlist.objects.filter(u_id=request.user, p_id=id)
        if w_data.exists():
            w_data.delete()

        messages.success(request, 'Product added to the cart!!')
        return redirect('/cart/')
    # return redirect('/cart/')
    
def deletecart(request,id):
    data=Cart.objects.get(u_id=request.user,crt_id=id)
    data.delete()
    messages.success(request,"Product deleted from cart")
    return redirect('/cart/')

def plus(request,id):
    data=Cart.objects.get(u_id=request.user,crt_id=id)
    data.quantity+=1
    if data.quantity>10:
        messages.error(request,"Quantity exceeded")
        return redirect('/cart/')

    data.save()
    return redirect('/cart/')

def minus(request,id):
    data=Cart.objects.get(u_id=request.user,crt_id=id)
    n=data.p_id.pname
    data.quantity-=1
    if data.quantity<1:
        data.delete()
        messages.success(request,n+" deleted from the cart.")
        return redirect('/cart/')
    data.save()
    return redirect('/cart/')

@login_required(login_url='/login/')
def wishlist(request):
    data=Wishlist.objects.filter(u_id=request.user)
   
    return render(request, 'wishlist.html',{'data':data})



@login_required(login_url='/login/')
def addtowishlist(request,id):
    data=Wishlist.objects.filter(u_id=request.user,p_id=id)

    if data:
        messages.error(request,"Product already in Wishlist")
        return redirect('/wishlist/')
    else:
        
        p=Product.objects.get(pid=id)
        s=Wishlist(p_id=p,u_id=request.user)
        s.save()
        messages.success(request,"Product added to Wishlist")
        return redirect('/wishlist/')
    
def deletewishlist(request,id):
    data=Wishlist.objects.get(u_id=request.user,w_id=id)
    data.delete()
    messages.success(request,"Product deleted from Wishlist")
    return redirect('/wishlist/')
def checkout(request):
    cdata=Cart.objects.filter(u_id=request.user).count()
    cart=Cart.objects.filter(u_id=request.user)
    if cdata==0:
        messages.error(request,'please add the data')
        return redirect('/cart/')
    # Calculate totals
    total_amount = sum(item.sub_total() for item in cart)
    charges = 50  # Assuming fixed shipping charges
    ftotal = total_amount + charges

    if (request.method=='POST'):
        fname=request.POST['fname']
        lname=request.POST['lname']
        email=request.POST['email']
        phone=request.POST['phone']
        address=request.POST['address']
        country=request.POST['country']
        city=request.POST['city']
        state=request.POST['state']
        zip=request.POST['zip']
        payment=request.POST['payment']
        amount=request.POST['amount']
        charges=request.POST['charges']
        id=O_tracker.objects.get(otid=1)
        s=Order(
                fname=fname,lname=lname,email=email,mobile=phone,address=address,city=city,
                state=state,country=country,zip=zip,payment=payment,amount=amount,order_status=id,charges=charges,u_id=request.user
                )
        s.save()
        last_order=Order.objects.last()
        card_data=Cart.objects.filter(u_id=request.user)

        for i in card_data:
            p=Product.objects.get(pid=i.p_id.pid)

            item_data=O_item(o_id=last_order,p_id=p,quantity=i.quantity,subtotal=i.sub_total())
            item_data.save()
            i.delete()
        return redirect('/confirmorder/'+str(s.oid))

    return render(request,'checkout.html',{'cart_data':cart, 'total_amount':total_amount, 'charges':charges, 'ftotal':ftotal})



def confirmorder(request,id):
    order_data=Order.objects.get(oid=id )
    order_item=Order.objects.filter(oid=id)
    return render(request,'confirmorder.html',{'order_data':order_data,'order_item':order_item})