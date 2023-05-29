import django
from django.http import HttpResponse,JsonResponse
from django.shortcuts import redirect, render,get_object_or_404
from accounts.models import UserProfile
from marketplace.context_processors import get_cart_counter,get_cart_amount
from marketplace.models import Cart


from vendor.models import Vendor
from menu.models import Category, FoodItem
from django.db.models import Prefetch
from django.contrib.auth.decorators import login_required
from django.db.models import Q

# Create your views here.

def is_ajax(request: django.http.request.HttpRequest) -> bool:
    """
    https://stackoverflow.com/questions/63629935
    """
    return (
        request.headers.get('x-requested-with') == 'XMLHttpRequest'
        or request.accepts("application/json")
    )

def marketplace(request):
    vendors = Vendor.objects.filter(is_approved=True,user__is_active=True)
    vendor_count=vendors.count()
    print(vendors)
    context={
        'vendors': vendors,
        'vendor_count': vendor_count,

    }
    return render(request,'marketplace/listing.html',context)


def vendor_detail(request, vendor_slug):
    vendor =get_object_or_404(Vendor,vendor_slug=vendor_slug)
    categories=Category.objects.filter(vendor=vendor).prefetch_related(
        Prefetch(
        'fooditems',
        queryset=FoodItem.objects.filter(is_available=True),
        )
    )

    if request.user.is_authenticated:
        cart_items=Cart.objects.filter(user=request.user)

    else:
        cart_items=None

    context={
        'vendor': vendor,
        'categories': categories,
        'cart_items': cart_items,

    }
    return render(request,'marketplace/vendor_detail.html',context)


def add_to_cart(requst,food_id):
    if requst.user.is_authenticated:
        if is_ajax(requst):
        #headers.get('x-requested-with') == 'XMLHttpRequest':
            #check if food is_available
            try:
                print(food_id)
                fooditem=FoodItem.objects.get(id=food_id)
                print(fooditem)
                #check if food alredy in cart
                try:
                    chkCart=Cart.objects.get(user=requst.user,fooditem=fooditem)
                    #increse quntity
                    chkCart.quantity +=1
                    chkCart.save()
                   
                    return  JsonResponse({'status':'Success','message':'qty encresed', 'cart_amount':get_cart_amount(requst),'cart_count':get_cart_counter(requst),'qty':chkCart.quantity})
                except:
                    chkCart=Cart.objects.create(user=requst.user,fooditem=fooditem,quantity=1)
                    
                    return    JsonResponse({'status':'Success','message':'food added to cart','cat_amount':get_cart_amount(requst),'cart_count':get_cart_counter(requst),'qty':chkCart.quantity})
                    
            except:
                return JsonResponse({'status':'Failed','message':'this food does not exist'})

        else:
             return JsonResponse({'status':'Failed','message':'Invalide request'})

      
    else:
        return JsonResponse({'status':'login_required','message':'Please login to continue'})
    

def decrease_cart(request,food_id):
    if request.user.is_authenticated:
        if is_ajax(request):
        #headers.get('x-requested-with') == 'XMLHttpRequest':
            #check if food is_available
            try:
                print(food_id)
                fooditem=FoodItem.objects.get(id=food_id)
                print(fooditem)
                #check if food alredy in cart
                try:
                    print(food_id)
                    chkCart=Cart.objects.get(user=request.user,fooditem=fooditem)
                    if chkCart.quantity > 1:
                    #decrease quntity
                        chkCart.quantity -= 1
                        chkCart.save()
                    else:
                        chkCart.delete()
                        chkCart.quantity = 0
                        
                       
                   
                    return  JsonResponse({'status':'Success','message':'qty decresed','cart_amount':get_cart_amount(request),'cart_count':get_cart_counter(request),'qty':chkCart.quantity})
                except:
                    
                    
                    return    JsonResponse({'status':'Failed','message':'You dont have thi item in ur cart'})
                    
            except:
                return JsonResponse({'status':'Failed','message':'this food does not exist'})

        else:
             return JsonResponse({'status':'Failed','message':'Invalide request'})

      
    else:
        return JsonResponse({'status':'login_required','message':'Please login to continue'})
    

@login_required(login_url='login')
def cart(request):
    cart_items=Cart.objects.filter(user=request.user).order_by('created_at')

    contex={
        'cart_items':cart_items,
    }
    return render(request,'marketplace/cart.html',contex)


def delete_cart(request,cart_id):
    if request.user.is_authenticated:
        if is_ajax(request):
            try:
                #check if cart item exist
                cart_item=Cart.objects.get(user=request.user,id=cart_id)
                if cart_item:
                    print('deleted')
                    cart_item.delete()
                    return JsonResponse({'status':'Success','message':'Cart item deleted!','cart_amount':get_cart_amount(request)})#'cart_counter':get_cart_counter(request)
            except:
                return JsonResponse({'status':'Failed','message':'Cart item does not exist'})
                    
        else:
            return JsonResponse({'status':'Failed','message':'Invalide request'})
        

def search(request):
    if not 'keyword' in request.GET:
        return redirect('marketplace')
    Keyword=request.GET['keyword']
    print('eeeee',Keyword)


    #get vendors that has the food item id



    vendors_by_fooditem=FoodItem.objects.filter(food_title__icontains=Keyword,is_available=True).values_list('vendor',flat=True)
    print(vendors_by_fooditem)

    vendors=Vendor.objects.filter(Q(id__in=vendors_by_fooditem) | Q(vendor_name__icontains=Keyword,is_approved=True,user__is_active=True))
    vendor_count=vendors.count()
    print(vendors)
    context={
        'vendors':vendors,
        'vendor_count':vendor_count,

    }
    return render(request,'marketplace/listing.html',context)



@login_required(login_url='login')
def payment(request):
  
     
    #if request.user.is_authenticated:
    return HttpResponse("Payment")



