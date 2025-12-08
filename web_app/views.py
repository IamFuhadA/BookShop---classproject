from django.shortcuts import render, redirect
from admin_app.models import CategoryDB, BookDB
from .models import RegistrationDB, ContactDB, CartDB, CheckoutDB
from django.contrib import messages


# ================= HOME PAGE ====================
def home_page(request):
    uname = request.session.get('username')
    total_items = 0

    if uname:
        total_items = CartDB.objects.filter(username=uname).count()

    category = {
        'categories': CategoryDB.objects.all(),
        'Books': BookDB.objects.all(),
        'cart_count': total_items
    }

    return render(request, "home.html", category)


# ================= ABOUT PAGE ====================
def about_page(request):
    uname = request.session.get('username')
    total_items = 0
    if uname:
        total_items = CartDB.objects.filter(username=uname).count()

    context = {
        'categories': CategoryDB.objects.all(),
        'cart_count': total_items
    }

    return render(request, "about.html", context)


# ================= POPULAR BOOKS PAGE ====================
def PopularBooks_page(request):
    uname = request.session.get('username')
    total_items = 0
    if uname:
        total_items = CartDB.objects.filter(username=uname).count()

    books = {
        'Books': BookDB.objects.all(),
        'categories': CategoryDB.objects.all(),
        'cart_count': total_items
    }

    return render(request, "popular_books.html", books)


# ================= CONTACT PAGE ====================
def Contact_Us(request):
    uname = request.session.get('username')
    total_items = 0
    if uname:
        total_items = CartDB.objects.filter(username=uname).count()

    context = {
        'categories': CategoryDB.objects.all(),
        'cart_count': total_items
    }

    return render(request, "contact.html", context)


def save_contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        mail = request.POST.get('email')
        sub = request.POST.get('subject')
        msg = request.POST.get('message')

        ContactDB.objects.create(
            name=name,
            mail=mail,
            subject=sub,
            message=msg
        )

        messages.success(request, "Saved successfully")
        return redirect(Contact_Us)


# ================= FILTER PAGE ====================
def filtered_page(request, book_category):
    uname = request.session.get('username')
    total_items = 0
    if uname:
        total_items = CartDB.objects.filter(username=uname).count()

    context = {
        'categories': CategoryDB.objects.all(),
        'books': BookDB.objects.filter(category=book_category),
        'filter': book_category,
        'cart_count': total_items
    }

    return render(request, "filtered_book.html", context)


# ================= SINGLE BOOK PAGE ====================
def single_book(request, book_id):
    uname = request.session.get('username')
    total_items = 0
    if uname:
        total_items = CartDB.objects.filter(username=uname).count()

    context = {
        'categories': CategoryDB.objects.all(),
        'single': BookDB.objects.get(id=book_id),
        'cart_count': total_items
    }

    return render(request, "book_details.html", context)


# ================= AUTH ====================
def signup_page(request):
    return render(request, "signup.html")


def save_signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        name = request.POST.get('name')
        mail = request.POST.get('email')
        contact = request.POST.get('number')
        password = request.POST.get('password')
        cnf_password = request.POST.get('confirm')

        # your validations unchanged
        if password != cnf_password:
            messages.error(request, 'Passwords do not match.')
            return redirect(signup_page)

        if RegistrationDB.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect(signup_page)

        if RegistrationDB.objects.filter(mail=mail).exists():
            messages.error(request, 'Email already registered.')
            return redirect(signup_page)

        if RegistrationDB.objects.filter(name=name).exists():
            messages.error(request, 'Name already registered.')
            return redirect(signup_page)

        RegistrationDB.objects.create(
            username=username,
            name=name,
            mail=mail,
            contact=contact,
            password=password,
            confirm_password=cnf_password
        )

        messages.success(request, 'Account created successfully!')
        return redirect(signin_page)


def signin_page(request):
    return render(request, "signin.html")


def signin(request):
    if request.method == "POST":
        name = request.POST.get('username')
        password = request.POST.get('password')

        if RegistrationDB.objects.filter(username=name, password=password).exists():
            request.session["username"] = name
            request.session["password"] = password
            messages.success(request, 'Welcome back!')
            return redirect(home_page)

        messages.error(request, 'Invalid username or password.')
        return redirect(signin_page)

    return redirect(signin_page)


def sign_out(request):
    request.session.flush()
    messages.info(request, 'You have been signed out successfully!')
    return redirect(home_page)


# ================= CART PAGE ====================
def cart_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        book_name = request.POST.get('title')
        quantity = int(request.POST.get('quantity'))
        price = int(request.POST.get('price'))
        total_price = int(request.POST.get('total'))

        book = BookDB.objects.filter(title=book_name).first()
        image = book.cover_image if book else None

        CartDB.objects.create(
            username=username,
            title=book_name,
            quantity=quantity,
            price=price,
            total_price=total_price,
            book_img=image
        )

        messages.success(request, 'Book added to cart successfully!')
        return redirect('cart_page')

    uname = request.session.get('username')
    context = CartDB.objects.filter(username=uname)

    total_items = CartDB.objects.filter(username=uname).count() if uname else 0

    # YOUR CART CALCULATION —— UNCHANGED
    sub_total = 0
    delivery_charge = 0
    total_amount = 0

    for i in context:
        sub_total += i.total_price
        if sub_total > 500:
            delivery_charge = 50
        else:
            delivery_charge = 100
        total_amount = sub_total + delivery_charge

    return render(request, "cart.html", {
        'data': context,
        'sub_total': sub_total,
        'delivery_charge': delivery_charge,
        'total_amount': total_amount,
        'cart_count': total_items
    })


def remove_cart(request, item_id):
    CartDB.objects.filter(id=item_id).delete()
    messages.success(request, 'Item removed from cart successfully!')
    return redirect('cart_page')


# ================= CHECKOUT PAGE ====================
def checkout_page(request):
    uname = request.session.get('username')
    data = CartDB.objects.filter(username=uname)

    sub_total = sum(i.total_price for i in data)
    delivery_charge = 50 if sub_total > 500 else 100
    total_amount = sub_total + delivery_charge

    total_items = CartDB.objects.filter(username=uname).count() if uname else 0

    if request.method == 'POST':
        CheckoutDB.objects.create(
            username=request.POST.get('fullname'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            address=request.POST.get('address'),
            sub_total=request.POST.get('sub_total'),
            delivery_charge=request.POST.get('delivery'),
            total_amount=request.POST.get('total_amount'),
            payment_type=request.POST.get('payment_type'),
        )
        messages.success(request, 'Order placed successfully! Proceeding to payment...')
        return redirect('payment')

    return render(request, "checkout.html", {
        'data': data,
        'sub_total': sub_total,
        'delivery_charge': delivery_charge,
        'total_amount': total_amount,
        'cart_count': total_items
    })


# ================= PAYMENT PAGE ====================
def payment_page(request):
    uname = request.session.get('username')
    cart_items = CartDB.objects.filter(username=uname)

    sub_total = sum(item.total_price for item in cart_items)
    delivery_charge = 50 if sub_total > 500 else 100
    total_amount = sub_total + delivery_charge

    return render(request, "payment.html", {
        'cart_items': cart_items,
        'sub_total': sub_total,
        'delivery_charge': delivery_charge,
        'total_amount': total_amount
    })
