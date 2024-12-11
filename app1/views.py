
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Product,CartItem
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email=request.POST['email']

        if User.objects.filter(username=username).exists():
            return HttpResponse('user exists')
        else:
            user = User(username=username,email=email)
            user.set_password(password)
            user.save()

            messages.success(request, "User registered successfully!")
            return redirect("/login")

    return render(request, "registration.html")


def user_login(request):
    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        user=User.objects.get(username=username)

        if user.check_password(password):

            request.session['my_user'] = username # 'my_user'= scession variable
            return redirect('product_list')

        else:

            return HttpResponse('Invalid credentials.')
    return render(request, 'userLogin.html')


def user_logout(request):
    request.session.flush() # clear session
    return redirect('login')

def product_list(request):
    if 'my_user' not in request.session:
        return redirect('login')
    products = Product.objects.all()
    return render(request, 'products_page.html', {'products': products})

def add_to_cart(request, product_id):

    if 'my_user' not in request.session:
        return redirect('login')

    username = request.session['my_user']
    user = User.objects.get(username=username)
    product = Product.objects.get(id=product_id)
    # print(username,user,product)
    # Add the product to the cart
    cart_item = CartItem.objects.filter(user=user, product=product).first()
    if cart_item:
        cart_item.quantity += 1
        cart_item.save()
    else:
        CartItem.objects.create(user=user,product=product,quantity=1)

    return redirect('view_cart')

def view_cart(request):
    if 'my_user' not in request.session:
        return redirect('login')

    username = request.session['my_user']
    user = User.objects.get(username=username)

    cart_items = CartItem.objects.filter(user=user)
    return render(request, 'cart.html', {'cart_items': cart_items})


def delete_from_cart(request, cart_item_id):

   cart_item = CartItem.objects.get(id=cart_item_id)

   # if cart_item:
   if cart_item.quantity > 1:
     cart_item.quantity -= 1
     cart_item.save()

   else:
       cart_item.delete()
   return redirect('view_cart')


