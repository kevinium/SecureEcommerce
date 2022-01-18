from django.shortcuts import render,get_object_or_404,redirect,HttpResponse
from django.db.models import Q
from .models import Item,OrderItem,Order,Payment,sellerItems
from signup.models import UserProfile
from django.views.generic import DetailView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin
from ecom.settings import RZP_API_KEY,RZP_SECRET_KEY,MEDIA_ROOT
import razorpay
from django.contrib.auth import get_user_model, login,logout
from django.views.decorators.csrf import csrf_exempt
from signup.models import seller,Admin
from signup.views import go_to_setup 
from .forms import addProductForm,addSellerForm,item_to_sellerform,update_user_address
import time
from django.http import FileResponse
import os
elaspsed=300
# Create your views here.
User=get_user_model()
def home_page(request):
    user_ = request.user 
    if(request.user.is_anonymous):
        context={
            'items':Item.objects.all()
        }
        return render(request,'buyer_homepage.html',context)
    if(len(seller.objects.filter(user = user_))!=0):
        item_list =[]
        item_list.extend(sellerItems.objects.filter(seller = user_)[0].item.all())
        context={
            'sellerItems':item_list
        }
        return render(request, 'seller_portal.html', context)
    if(is_admin(user_)):
        return redirect('/buyer/admin-home/')
    context={
        'items':Item.objects.all()
    }
    return render(request,'buyer_homepage.html',context)

class ItemDetailView(DetailView):
    model = Item
    template_name = "product_desc.html"

@login_required
def add_to_cart(request, slug):
    profile=UserProfile.objects.filter(user=request.user)[0]
    if profile.secret_string=='':
        return redirect('/setup-otp/')
    elif time.time()-profile.last_otp>=elaspsed:
        return redirect('/otp/')
    user_=request.user
    if((is_admin(user_) or is_seller(user_))):
        return redirect('/buyer/home')
    Buyer=request.user
    item = get_object_or_404(Item, slug=slug)
    order_item= OrderItem.objects.get_or_create(
        item=item,
        user=Buyer,
        ordered=False
    )[0]
    order_qs = Order.objects.filter(user=Buyer, ordered=False)
    #order_qs = Order.objects.filter(ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated.")
            #return redirect("core:order-summary")
        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            #return redirect("core:order-summary")
    else:
        order = Order.objects.create(user=Buyer)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
        #return redirect("core:order-summary")
    return redirect("buyer:product",slug=slug)




@login_required
def remove_from_cart(request, slug):
    
    profile=UserProfile.objects.filter(user=request.user)[0]
    if profile.secret_string=='':
        return redirect('/setup-otp/')
    elif time.time()-profile.last_otp>=elaspsed:
        return redirect('/otp/')
    user_=request.user
    if((is_admin(user_) or is_seller(user_))):
        return redirect('/buyer/home')
    
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, "This item was removed from your cart.")
            #return redirect("core:order-summary")
            return redirect("buyer:product", slug=slug)
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("buyer:product", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("buyer:product", slug=slug)


class OrderSummaryView(LoginRequiredMixin,DetailView):
    def get(self, *args, **kwargs):
        profile=UserProfile.objects.filter(user=self.request.user)[0]
        if profile.secret_string=='':
            return redirect('/setup-otp/')
        elif time.time()-profile.last_otp>=elaspsed:
            return redirect('/otp/')
        user_=self.request.user
        if((is_admin(user_) or is_seller(user_))):
            return redirect('/buyer/home')
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'order_summary.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("/buyer/home/")




@login_required
def remove_from_cart(request, slug):
    profile=UserProfile.objects.filter(user=request.user)[0]
    if profile.secret_string=='':
        return redirect('/setup-otp/')
    elif time.time()-profile.last_otp>=elaspsed:
        return redirect('/otp/')
    user_=request.user
    if((is_admin(user_) or is_seller(user_))):
        return redirect('/buyer/home')
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, "This item was removed from your cart.")
            return redirect("buyer:order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("buyer:product", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("buyer:product", slug=slug)


@login_required
def remove_single_item_from_cart(request, slug):
    profile=UserProfile.objects.filter(user=request.user)[0]
    if profile.secret_string=='':
        return redirect('/setup-otp/')
    elif time.time()-profile.last_otp>=elaspsed:
        return redirect('/otp/')
    user_=request.user
    if((is_admin(user_) or is_seller(user_))):
        return redirect('/buyer/home')
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This item quantity was updated.")
            return redirect("buyer:order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("buyer:product", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("buyer:product", slug=slug)

class CheckoutView(LoginRequiredMixin,DetailView):
    def get(self, *args, **kwargs):
        profile=UserProfile.objects.filter(user=self.request.user)[0]
        if profile.secret_string=='':
            return redirect('/setup-otp/')
        elif time.time()-profile.last_otp>=elaspsed:
            return redirect('/otp/')
        user_=self.request.user
        if((is_admin(user_) or is_seller(user_))):
            return redirect('/buyer/home')
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'pre_payment.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("/buyer/home/")


@login_required
def pay(request):
    profile=UserProfile.objects.filter(user=request.user)[0]
    if profile.secret_string=='':
        return redirect('/setup-otp/')
    elif time.time()-profile.last_otp>=elaspsed:
        return redirect('/otp/')
    order_amount=0
    user_=request.user
    if((is_admin(user_) or is_seller(user_))):
        return redirect('/buyer/home')
    try:
        order = Order.objects.get(user=request.user, ordered=False)
        order_amount=order.get_total()*100
    except ObjectDoesNotExist:
            messages.warning(request, "You do not have an active order")
            return redirect("/buyer/home/")
    client = razorpay.Client(auth=(RZP_API_KEY,RZP_SECRET_KEY))

    payment_order=client.order.create(dict(amount=order_amount,currency='INR',payment_capture=0))
    payment_order_id=payment_order['id']

    payment=Payment()
    payment.user=request.user
    
    payment.amount=order_amount/100
    payment.order_id=payment_order_id
    payment.save()

    order.payment=payment

    order.save()

    #Order=order(amount=amount,order_id=payment_order_id)
    #Order.save()

    #callback_url='http://'+str(get_current_site(request))+ 'payment_success/'
    callback_url=request.build_absolute_uri()+'payment-status/'
    context={
        'amount':order_amount/100,'api_key':RZP_API_KEY,'order_id':payment_order_id,'callback_url':callback_url
    }
    return render(request,'payment.html',context)


@csrf_exempt
@login_required
def payment_status(request):
    profile=UserProfile.objects.filter(user=request.user)[0]
    if profile.secret_string=='':
        return redirect('/setup-otp/')
    elif time.time()-profile.last_otp>=elaspsed:
        return redirect('/otp/')
    user_=request.user
    if((is_admin(user_) or is_seller(user_))):
        return redirect('/buyer/home')
    response = request.POST
    params_dict = {
        'razorpay_order_id': response['razorpay_order_id'],
        'razorpay_payment_id': response['razorpay_payment_id'],
        'razorpay_signature': response['razorpay_signature']
    }

    # client instance
    client = razorpay.Client(auth=(RZP_API_KEY,RZP_SECRET_KEY))

    try:
        client.utility.verify_payment_signature(params_dict)
        payment = Payment.objects.get(order_id=response['razorpay_order_id'])
        payment.razorpay_order_id = response['razorpay_payment_id']
        order=Order.objects.get(user=request.user, ordered=False)

        order_items = order.items.all()
        order_items.update(ordered=True)
        for item in order_items:
                item.save()

        order.ordered = True

        order.save()
        payment.save()

        amt=payment.amount
        client.payment.capture(payment.razorpay_order_id,amt*100)
        #return HttpResponse("Success!")
        return redirect('/buyer/pay/payment-status/success')
    except:
        #return HttpResponse("Failed!")
        return redirect('/buyer/pay/payment-status/failure')
    
@login_required
def profile(request):
    user_=request.user
    if((is_admin(user_) or is_seller(user_))):
        return redirect('/buyer/home')
    profile=UserProfile.objects.filter(user=request.user)[0]
    if profile.secret_string=='':
        return redirect('/setup-otp/')
    elif time.time()-profile.last_otp>=elaspsed:
        return redirect('/otp/')
    context={
        'name':request.user.username, 'address':profile.address
    }
    return render(request,'profile.html',context)


@login_required
def payment_status_success(request):
    return render(request,'success.html')

@login_required
def payment_status_failure(request):
    return render(request,'failure.html')


def search(request):
    query=str(request.GET['Search']).split(" ")
    Item_list=[]
    for q in query:
        Item_list.extend(Item.objects.filter(Q(title__icontains=q) | Q(description__icontains=q)))
    
    if(len(Item_list)==0):
        return redirect(request,'/buyer/home')
    else:
        context={
        'items':Item_list
    }
    return render(request,'buyer_homepage.html',context)
        
     

def add_prod(request):
    # Check for seller
    # if yes then allow
    # otherwise redirect to homepage
    user_=request.user
    if(not is_seller(user_)):
        return redirect('/buyer/home')
    if(request.user.is_anonymous):
        return redirect('/accounts/login/')
    if request.method == 'POST':
        form = addProductForm(request.POST, request.FILES)
        

        if(form.is_valid()):
            form.save()
            print(form.cleaned_data['slug'])
            # item_to_seller_form = item_to_sellerform()
            # item_to_seller_form.seller=request.user
            # item_to_seller_form.item = get_object_or_404(Item, slug=form.slug)
            # item_to_seller_form.save()
            #         order_qs = Order.objects.filter(user=Buyer, ordered=False)
            # #order_qs = Order.objects.filter(ordered=False)
            # if order_qs.exists():
            #     order = order_qs[0]
            #     if order.items.filter(item__slug=item.slug).exists():
            #         order_item.quantity += 1
            #         order_item.save()
            #         messages.info(request, "This item quantity was updated.")
            #         #return redirect("core:order-summary")
            #     else:
            #         order.items.add(order_item)
            #         messages.info(request, "This item was added to your cart.")
            #         #return redirect("core:order-summary")
            # else:
            #     order = Order.objects.create(user=Buyer)
            #     order.items.add(order_item)
            seller_it = sellerItems.objects.filter(seller=request.user)
            if seller_it.exists():
                seller_it = sellerItems.objects.get(seller=request.user)
                seller_it.item.add(get_object_or_404(Item, slug=form.cleaned_data['slug']))
                seller_it.save()
            else:
                seller_it = sellerItems.objects.create(seller=request.user)
                seller_it.item.add(get_object_or_404(Item, slug=form.cleaned_data['slug']))
                seller_it.save()

            return redirect('/buyer/home')
    else:
        form  = addProductForm()
    return render(request, 'add_product.html', {'form':form})

@login_required
def addSeller(request):
    if(request.user.is_anonymous):
        return redirect('/accounts/login/')
    if(len(seller.objects.filter(user = request.user))!=0):
        return seller_page(request)
    if is_admin(request.user):
        return redirect('/buyer/home')
    if request.method == 'POST':
        form = addSellerForm(request.POST, request.FILES)
        #form.User = request.user
        #form['user']= request.user
        try: 
            if form.is_valid:
                #seller1 = seller(User=request.user,)
                print("valid")
                form.save()
                seller1 = seller.objects.create(user=request.user, pdf = request.FILES['pdf']) 
                seller1.save()
                seller_it = sellerItems.objects.create(seller=request.user)
                seller_it.save()
                
                return redirect('/buyer/home/',request)
            else:
                form = addSellerForm()
            return render(request, 'upg_seller.html', {'form':form})

        except ValueError:
            form = addSellerForm()
            messages.info(request, "Please upload a valid pdf")
            return render(request, 'upg_seller.html', {'form':form})

            

    else:
        form = addSellerForm()
    return render(request, 'upg_seller.html', {'form':form})


def logout_view(request):
    user_ = request.user 
    logout(request)
    return redirect('/accounts/login/')


def seller_page(request, context):
    if request.method == 'POST':
        user_ = request.user 
        logout(request)
        return redirect('/accounts/login/')
    if not is_seller(request.user):
        return redirect('/buyer/home/')
    return render(request, 'seller_portal.html', context)

@login_required
def admin_view(request):
    user_=request.user
    if(not is_admin(user_)):
        return redirect('/buyer/home/')
    context={
        'items':Item.objects.all(),
        'profiles':UserProfile.objects.filter(otp_count__gte=5),
        'sellers':seller.objects.all(),
    }
    return render(request, 'adminhome.html', context)

@login_required
def reset_account(request,slug):
    user_=request.user
    if(not is_admin(user_)):
        return redirect('/buyer/home/')
    user=User.objects.get(username=slug)
    profile = get_object_or_404(UserProfile, user=user)
    profile.otp_count=0
    profile.save()
    messages.info(request,'Account reset done')
    return redirect('/buyer/admin-home/')
    
@login_required
def open_pdf(request,slug):
    user_=request.user
    if(not is_admin(user_)):
        return redirect('/buyer/home/')
    filepath = os.path.join(MEDIA_ROOT+'/pdf/',slug)
    print(filepath)
    return FileResponse(open(filepath, 'rb'))

@login_required
def remove_item(request,slug):
    user_=request.user
    if(not is_admin(user_)):
        return redirect('/buyer/home/')
    qs=Item.objects.filter(slug=slug)
    if(qs.exists()):
        item=qs[0]
        for obj in sellerItems.objects.all():
            seller=obj
            seller_items=seller.item.all()
            if ( item in seller_items):
                seller.item.remove(item)
        
        item.delete()
        messages.info(request,'Item delete')

    return redirect('/buyer/admin-home/')

@login_required
def update_address(request):
    if request.method == 'POST':
        form = update_user_address(request.POST)
        if form.is_valid():
            user_prof = UserProfile.objects.get(user=request.user)
            user_prof.address = form.cleaned_data['address']
            user_prof.save()
            if( is_seller(request.user)):
                return redirect('/buyer/home/')
            return redirect('/buyer/profile/')
    else:
        form = update_user_address()
    return render(request, 'update_address.html', {'form':form})


def is_seller(user_):
    return (len(seller.objects.filter(user = user_))!=0)

def is_admin(user_):
    return (len(Admin.objects.filter(user = user_))!=0)