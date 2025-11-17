from django.shortcuts import render,redirect
from .models import CategoryDB,BookDB
from django.core.files.storage import FileSystemStorage
from django.utils.datastructures import MultiValueDictKeyError
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from web_app.models import ContactDB
# Create your views here.
def index(request):
    date = datetime.now().strftime("%b %d, %Y")
    book=BookDB.objects.count()
    category=CategoryDB.objects.count()
    return render(request,"index.html",{'date':date,'book':book,'category':category})

def login_page(request):
    return render(request,"login.html")

def admin_login(request):
    if request.method == "POST":
        name = request.POST.get('username')
        pasd = request.POST.get('password')
        if User.objects.filter(username__contains=name).exists():
            data = authenticate(username=name,password=pasd)
            if data is not None:
                login(request,data)
                request.session["username"]=name
                request.session["password"]=pasd
                return redirect(index)
            else:
                return redirect(login_page)
    else:
        return redirect(login_page)

def logout_page(request):
    del request.session['username']
    del request.session['password']
    return redirect(login_page)


#------------------------------------------------------------------------------------------

def add_category(request):
    number = CategoryDB.objects.count()
    return render(request,"add_category.html",{'number':number})

def save_category(request):
    if request.method == "POST":
        name = request.POST.get('name')
        dcpn = request.POST.get('dcpn')
        img = request.FILES.get('img')
        obj = CategoryDB(
            category_name =name,
            Description = dcpn,
            cover_image =img ,
        )
        obj.save()
        return redirect(add_category)

def display_category(request):
    data = CategoryDB.objects.all()
    return render(request,"display_category.html",{'data':data})

def edit_category(request,u_id):
    cat = CategoryDB.objects.get(id=u_id)
    return render(request,"edit_category.html",{'cat':cat})

def update_category(request,u_id):
    if request.method == "POST":
        name = request.POST.get('name')
        dcpn = request.POST.get('dcpn')
        try:
            img_set = request.FILES['img']
            file = FileSystemStorage()
            filename=file.save(img_set.name,img_set)
        except MultiValueDictKeyError:
            filename = CategoryDB.objects.get(id=u_id).cover_image
        CategoryDB.objects.filter(id=u_id).update(
            category_name =name,
            Description = dcpn,
            cover_image =filename ,
        )
        return redirect(display_category)

def delete_category(request,d_id):
    cate = CategoryDB.objects.get(id=d_id)
    cate.delete()
    return redirect(display_category)

#------------------------------------------------------

def add_book(request):
    categories = CategoryDB.objects.all()
    return render(request,"add_book.html",{'categories':categories})

def save_book(request):
    if request.method == "POST":
        title = request.POST.get('title')
        author = request.POST.get('author')
        category = request.POST.get('category')
        price = request.POST.get('price')
        publisher = request.POST.get('publisher')
        description = request.POST.get('description')
        img = request.FILES.get('img')

        obj = BookDB(
            title=title,
            author=author,
            category=category,
            price=price,
            publisher=publisher,
            description=description,
            cover_image=img
        )
        obj.save()
        return redirect(add_book)

def display_book(request):
    data = BookDB.objects.all()
    return render(request,"display_book.html",{'data':data})

def edit_book(request, b_id):
    book = BookDB.objects.get(id=b_id)
    categories = CategoryDB.objects.all()
    return render(request, "edit_book.html", {'book': book, 'categories': categories})


def update_book(request, b_id):
    if request.method == "POST":
        title = request.POST.get('title')
        author = request.POST.get('author')
        category = request.POST.get('category')
        price = request.POST.get('price')
        publisher = request.POST.get('publisher')
        description = request.POST.get('description')

        try:
            img = request.FILES['cover_image']
            file = FileSystemStorage()
            filename = file.save(img.name, img)
        except MultiValueDictKeyError:
            filename = BookDB.objects.get(id=b_id).cover_image

        BookDB.objects.filter(id=b_id).update(
            title=title,
            author=author,
            category=category,
            price=price,
            publisher=publisher,
            description=description,
            cover_image=filename
        )

        return redirect('display_book')


def delete_book(request, b_id):
    BookDB.objects.filter(id=b_id).delete()
    return redirect('display_book')

#-----------------------------------------------------
def message(request):
    data = {
        'data': ContactDB.objects.all()
    }
    return render(request, "message.html", data)

def delete_message(request, m_id):
    ContactDB.objects.filter(id=m_id).delete()
    return redirect('message')