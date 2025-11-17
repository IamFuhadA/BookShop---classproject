from django.shortcuts import render,redirect
from admin_app.models import CategoryDB,BookDB
from .models import RegistrationDB,ContactDB,CartDB
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

# Create your views here.

def home_page(request):
    category = {
        'categories':CategoryDB.objects.all(),
        'Books': BookDB.objects.all(),
    }
    return render(request,"home.html",category)

def about_page(request):
    category = {'categories': CategoryDB.objects.all()}
    return render(request,"about.html",category)

def PopularBooks_page(request):
    books = {
        'Books':BookDB.objects.all(),
        'categories': CategoryDB.objects.all()
    }
    return render(request,"popular_books.html",books)

def Contact_Us(request):
    category = {'categories': CategoryDB.objects.all()}
    return render(request,"contact.html",category)

def save_contact(request):
    if request.method=="POST":
        name = request.POST.get('name')
        mail = request.POST.get('email')
        sub = request.POST.get('subject')
        msg = request.POST.get('message')
        obj = ContactDB(name=name,mail=mail,subject=sub,message=msg)
        obj.save()
        return redirect(Contact_Us)

def filtered_page(request,book_category):
    category = {'categories': CategoryDB.objects.all(),
                'books':BookDB.objects.filter(category=book_category),
                'filter':book_category
                }
    return render(request,"filtered_book.html",category)

def single_book(request,book_id):
    category = {
        'categories': CategoryDB.objects.all(),
        'single':BookDB.objects.get(id=book_id)
                }
    return render(request,"book_details.html",category)


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

        obj = RegistrationDB(
            username=username,name=name,
            mail=mail,contact=contact,password=password,
            confirm_password=cnf_password
        )
        if RegistrationDB.objects.filter(name=name).exists():
            return redirect(signup_page)
        elif RegistrationDB.objects.filter(mail=mail).exists():
            return redirect(signup_page)
        elif RegistrationDB.objects.filter(username=username).exists():
            return redirect(signup_page)
        else :
            obj.save()
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
            return redirect(home_page)
        else:
            return redirect(signin_page)
    else:
        return redirect(signin_page)

def sign_out(request):
    del request.session["username"]
    del request.session["password"]
    return redirect(signin_page)

#-----------------------------------------------

def cart_page(request):
    return render(request,"cart.html")
