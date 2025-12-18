from django.shortcuts import render,redirect
from pyexpat.errors import messages
from .models import CategoryDB,BookDB
from django.core.files.storage import FileSystemStorage
from django.utils.datastructures import MultiValueDictKeyError
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from web_app.models import ContactDB, CheckoutDB
from django.contrib import messages


# Create your views here.
def index(request):
    date = datetime.now().strftime("%b %d, %Y")
    book=BookDB.objects.count()
    category=CategoryDB.objects.count()
    message_count = ContactDB.objects.count()
    purchase_count = CheckoutDB.objects.count()
    return render(request,"index.html",{
        'date':date,
        'book':book,
        'category':category,
        'message_count': message_count,
        'purchase_count': purchase_count
    })

def login_page(request):
    return render(request,"login.html")


def admin_login(request):
    if request.method == "POST":
        name = request.POST.get('username')
        pasd = request.POST.get('password')

        # Backend validation
        if not name or not name.strip():
            messages.error(request, "Username is required")
            return redirect(login_page)
        
        if not pasd:
            messages.error(request, "Password is required")
            return redirect(login_page)

        # Check if user exists
        if User.objects.filter(username=name).exists():
            data = authenticate(username=name, password=pasd)

            if data is not None:
                login(request, data)
                request.session["username"] = name
                messages.success(request, "Signed in Successfully")
                return redirect(index)  # use url name
            else:
                messages.error(request, "Invalid Password")
                return redirect(login_page)

        else:
            messages.error(request, "User does not exist")
            return redirect(login_page)




def logout_page(request):
    del request.session['username']
    del request.session['password']
    messages.success(request,"Logged out successfully")
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
        
        # Backend validation
        if not name or not name.strip():
            messages.error(request, 'Category name is required')
            return redirect(add_category)
        
        if not dcpn or not dcpn.strip():
            messages.error(request, 'Description is required')
            return redirect(add_category)
        
        if not img:
            messages.error(request, 'Cover image is required')
            return redirect(add_category)
        
        # Check for duplicate category
        if CategoryDB.objects.filter(category_name=name).exists():
            messages.error(request, 'Category with this name already exists')
            return redirect(add_category)
        
        obj = CategoryDB(
            category_name =name,
            Description = dcpn,
            cover_image =img ,
        )
        obj.save()
        messages.success(request,"Category saved successfully!")
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
        messages.success(request, 'Category updated successfully!')
        return redirect(display_category)

def delete_category(request,d_id):
    cate = CategoryDB.objects.get(id=d_id)
    cate.delete()
    messages.error(request, "Deleted successfully...!")
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
        
        # Backend validation
        if not title or not title.strip():
            messages.error(request, 'Title is required')
            return redirect(add_book)
        
        if not author or not author.strip():
            messages.error(request, 'Author is required')
            return redirect(add_book)
        
        if not category or category.strip() == "":
            messages.error(request, 'Please select a category')
            return redirect(add_book)
        
        if not price or not price.strip():
            messages.error(request, 'Price is required')
            return redirect(add_book)
        
        try:
            price_val = int(price)
            if price_val <= 0:
                messages.error(request, 'Price must be greater than zero')
                return redirect(add_book)
        except ValueError:
            messages.error(request, 'Please enter a valid price')
            return redirect(add_book)
        
        if not publisher or not publisher.strip():
            messages.error(request, 'Publisher is required')
            return redirect(add_book)
        
        if not description or not description.strip():
            messages.error(request, 'Description is required')
            return redirect(add_book)
        
        if not img:
            messages.error(request, 'Cover image is required')
            return redirect(add_book)
        
        # Check for duplicate title
        if BookDB.objects.filter(title=title).exists():
            messages.error(request, 'A book with this title already exists')
            return redirect(add_book)

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
        messages.success(request, 'Book added successfully!')
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

        messages.success(request, 'Book updated successfully!')
        return redirect('display_book')


def delete_book(request, b_id):
    BookDB.objects.filter(id=b_id).delete()
    messages.warning(request, 'Book deleted successfully!')
    return redirect('display_book')

#-----------------------------------------------------
def message(request):
    data = {
        'data': ContactDB.objects.all()
    }
    return render(request, "message.html", data)

def delete_message(request, m_id):
    ContactDB.objects.filter(id=m_id).delete()
    messages.success(request, 'Message deleted successfully!')
    return redirect('message')

#-----------------------------------------------------
def display_purchases(request):
    """Display all purchases/orders in admin dashboard"""
    data = {
        'data': CheckoutDB.objects.all().order_by('-id')
    }
    return render(request, "display_purchases.html", data)