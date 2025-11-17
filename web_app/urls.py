from django.urls import path
from . import views

urlpatterns=[

    path('home/',views.home_page,name='home'),
    path('about/',views.about_page,name='about'),
    path('books/',views.PopularBooks_page,name='books'),
    path('contact/', views.Contact_Us, name='contact'),
    path('save_contact/', views.save_contact, name='save_contact'),
    path('category/<book_category>/', views.filtered_page, name='categories'),
    path('details/<int:book_id>/', views.single_book, name='details'),
    path('cart/',views.cart_page,name="cart"),

    # Auth
    path('signup/', views.signup_page, name='signup'),
    path('save_signup/', views.save_signup, name='save_signup'),
    path('signin/', views.signin_page, name='signin'),
    path('signin_in/', views.signin, name='signin_in'),
    path('signin_out/', views.sign_out, name='signin_out'),

]