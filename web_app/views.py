from django.shortcuts import render,redirect
from admin_app.models import CategoryDB,BookDB
from .models import RegistrationDB,ContactDB,CartDB
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.

def home_page(request):

    uname = request.session.get('username')
    total_items = 0  # always define first

    if uname:
        total_items = CartDB.objects.filter(username=uname).count()

    category = {
        'categories': CategoryDB.objects.all(),
        'Books': BookDB.objects.all(),
        'cart_count': total_items
    }

    return render(request, "home.html", category)


def about_page(request):
    category = {'categories': CategoryDB.objects.all()}
    uname = request.session.get('username')
    total_items = 0  # always define first

    if uname:
        total_items = CartDB.objects.filter(username=uname).count()
    return render(request,"about.html",category,{'cart_count': total_items})

def PopularBooks_page(request):
    books = {
        'Books':BookDB.objects.all(),
        'categories': CategoryDB.objects.all()
    }
    uname = request.session.get('username')
    total_items = 0  # always define first

    if uname:
        total_items = CartDB.objects.filter(username=uname).count()
    return render(request,"popular_books.html",books ,{'cart_count': total_items})

def Contact_Us(request):
    category = {'categories': CategoryDB.objects.all()}
    uname = request.session.get('username')
    total_items = 0  # always define first

    if uname:
        total_items = CartDB.objects.filter(username=uname).count()
    return render(request,"contact.html",category,{'cart_count': total_items})

def save_contact(request):
    if request.method=="POST":
        name = request.POST.get('name')
        mail = request.POST.get('email')
        sub = request.POST.get('subject')
        msg = request.POST.get('message')
        obj = ContactDB(name=name,mail=mail,subject=sub,message=msg)
        obj.save()
        messages.success(request,"Saved successfully")
        return redirect(Contact_Us)

def filtered_page(request,book_category):
    category = {'categories': CategoryDB.objects.all(),
                'books':BookDB.objects.filter(category=book_category),
                'filter':book_category
                }
    uname = request.session.get('username')
    total_items = 0  # always define first

    if uname:
        total_items = CartDB.objects.filter(username=uname).count()
    return render(request,"filtered_book.html",category,{'cart_count': total_items})

def single_book(request,book_id):
    category = {
        'categories': CategoryDB.objects.all(),
        'single':BookDB.objects.get(id=book_id)
                }
    uname = request.session.get('username')
    total_items = 0  # always define first

    if uname:
        total_items = CartDB.objects.filter(username=uname).count()
    return render(request,"book_details.html",category,{'cart_count': total_items})


# ---------------------------------------------------------------------
def signup_page(request):
    # if request.user.is_authenticated:
    #     return redirect(home_page)
    return render(request, "signup.html")

def save_signup(request):
    if request.method == "POST":
        username=request.POST.get('username')
        name=request.POST.get('name')
        mail=request.POST.get('email')
        contact=request.POST.get('number')
        password=request.POST.get('password')
        cnf_password=request.POST.get('confirm')

        # Validate password match
        if password != cnf_password:
            messages.error(request, 'Passwords do not match. Please try again.')
            return redirect(signup_page)
        # Check for duplicate username
        if RegistrationDB.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists. Please choose a different username.')
            return redirect(signup_page)
        # Check for duplicate email
        if RegistrationDB.objects.filter(mail=mail).exists():
            messages.error(request, 'Email already registered. Please use a different email.')
            return redirect(signup_page)
        # Check for duplicate name
        if RegistrationDB.objects.filter(name=name).exists():
            messages.error(request, 'This name is already registered.')
            return redirect(signup_page)

        # Create new user
        obj = RegistrationDB(
            username=username,name=name,
            mail=mail,contact=contact,password=password,
            confirm_password=cnf_password
        )
        obj.save()
        messages.success(request, 'Account created successfully! Please sign in.')
        return redirect(signin_page)

#-----------------------------------------------------------------------
def signin_page(request):
    return render(request, "signin.html")

def signin(request):
    if request.method == "POST":
        name = request.POST.get('username')
        password= request.POST.get('password')
        if RegistrationDB.objects.filter(username=name,password=password).exists():
            request.session["username"]=name
            request.session["password"]=password
            messages.success(request, f'Welcome back! You have successfully signed in.')
            return redirect(home_page)
        else:
            messages.error(request, 'Invalid username or password. Please try again.')
            return redirect(signin_page)
    else:
        return redirect(signin_page)

def sign_out(request):
    del request.session["username"]
    del request.session["password"]
    return redirect(home_page)

#-----------------------------------------------

def cart_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        book_name = request.POST.get('title')
        quantity = int(request.POST.get('quantity'))
        price = int(request.POST.get('price'))
        total_price = int(request.POST.get('total'))

        book = BookDB.objects.filter(title=book_name).first()
        image = book.cover_image if book else None

        obj=CartDB(
            username=username,
            title=book_name,
            quantity=quantity,
            price=price,
            total_price=total_price,
            book_img=image
        )
        obj.save()
        return redirect('cart_page')

    context = CartDB.objects.filter(username=request.session.get('username'))

    uname = request.session.get('username')
    total_items = 0  # always define first

    if uname:
        total_items = CartDB.objects.filter(username=uname).count()

    sub_total=0
    delivery_charge=0
    total_amount=0
    for i in context:
        sub_total += i.total_price
        if sub_total > 500:
            delivery_charge=50
        else :
            delivery_charge=100
        total_amount= sub_total+delivery_charge

    return render(request, "cart.html", {'data':context , 'sub_total':sub_total ,
                                         'delivery_charge':delivery_charge,
                                         'total_amount':total_amount,
                                         'cart_count': total_items,
                                         })

def remove_cart(request, item_id):
    CartDB.objects.filter(id=item_id).delete()
    return redirect('cart_page')

def checkout_page(request):
    uname = request.session.get('username')
    data = CartDB.objects.filter(username=uname)

    sub_total = sum(i.total_price for i in data)
    delivery_charge = 50 if sub_total > 500 else 100
    total_amount = sub_total + delivery_charge
    total_items = 0  # always define first

    if uname:
        total_items = CartDB.objects.filter(username=uname).count()

    return render(request, "checkout.html", {
        'data': data,
        'sub_total': sub_total,
        'delivery_charge': delivery_charge,
        'total_amount': total_amount,
        'cart_count': total_items,
    })
