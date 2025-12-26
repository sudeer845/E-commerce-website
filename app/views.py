from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse
from . models import Product, Customer, Cart, Wishlist
from .forms import CustomerRegistrationForm,CustomerProfileForm
from django.contrib import messages
from django.contrib.auth import logout
from django.db.models import Q
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='login')
def home(request):
    return render(request,"app/home.html")

def about(request):
    totalitem=0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request,"app/about.html",locals())

def contact(request):
    totalitem=0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request,"app/contact.html",locals())

class CategoryView(View):
    def get(self,request,val):
        totalitem=0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        product = Product.objects.filter(category=val)
        title = Product.objects.filter(category=val).values('title')
        return render(request,"app/category.html",locals())

class CategoryTitle(View):
    def get(self,request,val):
        product = Product.objects.filter(title=val)
        title = Product.objects.filter(category=product[0].category).values('title')
        totalitem=0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        return render(request,"app/category.html",locals())

class ProductDetail(View):
    def get(self,request,pk):
        totalitem=0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        product = Product.objects.get(pk=pk)
        wishlist = Wishlist.objects.filter(Q(product=product)& Q(user=request.user))
        return render(request,"app/productdetail.html",locals())
    
class CustomerRegistrationView(View):
    def get(self,request):   
        form = CustomerRegistrationForm()
        return render(request,'app/customerregistration.html',locals())
    def post(self,request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Congratulations! User Registration Successfully")
        else:
            messages.error(request,"Invalid Input Data")
        return render(request,'app/customerregistration.html',locals())
    
class ProfileView(View):
    def get(self,request):
        form = CustomerProfileForm() 
        return render(request,'app/profile.html',locals())
    def post(self,request):
        form = CustomerProfileForm(request.POST) 
        if form.is_valid():
            user=request.user
            name=form.cleaned_data['name']
            locality=form.cleaned_data['locality']
            city=form.cleaned_data['city']
            mobile=form.cleaned_data['mobile']
            state=form.cleaned_data['state']
            pincode=form.cleaned_data['pincode']

            reg=Customer(
                user=user,
                name=name,
                locality=locality,
                city=city,
                mobile=mobile,
                state=state,
                pincode=pincode
                )
            reg.save()
            messages.success(request,"Congratulations! Profile Save Successfully")
        else:
            messages.warning(request,"Invalid Data")

        return render(request,'app/profile.html',locals())

def address(request):
    add = Customer.objects.filter(user=request.user)
    return render (request,'app/address.html',locals())

class updateAddress(View):
    def get(self,request,pk):
        add=Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=add)
        return render(request,'app/updateAddress.html',locals())
    def post(self,request,pk):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            # print('form is valid')
            add = Customer.objects.get(pk=pk)
            add.name=form.cleaned_data['name']
            add.locality=form.cleaned_data['locality']
            add.city=form.cleaned_data['city']
            add.mobile=form.cleaned_data['mobile']
            add.state=form.cleaned_data['state']
            add.pincode=form.cleaned_data['pincode']
            add.save()

            messages.success(request,"Congratulations! Profile Save Successfully")
        else:
            messages.warning(request,"Invalid Data")
        return redirect('address')
    
def LogoutView(request):
    logout(request)
    return redirect('login')

def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id = product_id)
    Cart(user = user, product = product).save()
    return redirect("/cart")

def show_cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0
    for p in cart:
        value = p.quantity*p.product.discount_price
        amount = amount+value
    totalamount = amount+40
    return render(request,'app/addtocart.html',locals())

class checkout(View):
    def get(self,request):
        user=request.user
        add = Customer.objects.filter(user=user)
        cart_items = Cart.objects.filter(user=user)
        famount=0
        for p in cart_items:
            value = p.quantity*p.product.discount_price
            famount = famount+value
        totalamount = famount+40
        return render(request,'app/checkout.html',locals())

def plus_cart(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        print(prod_id)
        c = Cart.objects.get(Q(product=prod_id)& Q(user=request.user))
        c.quantity+=1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity*p.product.discount_price
            amount = amount+value
        totalamount = amount+40
        data = {
            'quantity': c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)
    
def minus_cart(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        print(prod_id)
        c = Cart.objects.get(Q(product=prod_id)& Q(user=request.user))
        c.quantity-=1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity*p.product.discount_price
            amount = amount+value
        totalamount = amount+40
        data = {
            'quantity': c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)
    

def remove_cart(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        print(prod_id)
        c = Cart.objects.get(Q(product=prod_id)& Q(user=request.user))
        c.delete()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discount_price
            amount = amount + value
        totalamount = amount + 40
        data = {
            'quantity': c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)

@login_required(login_url='/login/')
def plus_wishlist(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'You must be logged in to modify wishlist'})
    if request.method == "GET":
        prod_id = request.GET['prod_id']
        product = Product.objects.get(id=prod_id)
        w = Wishlist(user=request.user,product=product)
        w.save()
        data={
            'message':'Whislist Added Successfully'
        }
        return JsonResponse(data)
    
def minus_wishlist(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'You must be logged in to modify wishlist'})
    if request.method == "GET":
        prod_id = request.GET['prod_id']
        product = Product.objects.get(id=prod_id)
        Wishlist_item=Wishlist.objects.filter(user=request.user,product=product)
        Wishlist_item.delete()
        data={
            'message':'Whislist Removed Successfully'
        }
        return JsonResponse(data)
    
def search(request):
    query = request.GET.get('search', '')  
    products = Product.objects.filter(Q(title__icontains=query)) if query else Product.objects.none()
    context = {
        'query': query,
        'products': products,
    }
    return render(request, 'app/search.html', context)

    