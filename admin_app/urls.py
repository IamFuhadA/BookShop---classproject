from django.urls import path
from . import views

urlpatterns=[
    path('home/',views.index,name='home'),
    path('login/',views.login_page,name='login'),
    path('admin_login/',views.admin_login,name='admin_login'),
    path('logout/',views.logout_page,name='logout'),

    path('category/',views.add_category,name='add_category'),
    path('save_category/',views.save_category,name='save_category'),
    path('display_category/',views.display_category,name='display_category'),
    path('edit_category/<int:u_id>/',views.edit_category,name='edit_category'),
    path('update_category/<int:u_id>/',views.update_category,name='update_category'),
    path('delete_category/<int:d_id>/',views.delete_category,name='delete_category'),


    path('bookdb/',views.add_book,name='bookdb'),
    path('save_book/', views.save_book, name='save_book'),
    path('display_book/', views.display_book, name='display_book'),
    path('edit_book/<int:b_id>/', views.edit_book, name='edit_book'),
    path('update_book/<int:b_id>/', views.update_book, name='update_book'),
    path('delete_book/<int:b_id>/', views.delete_book, name='delete_book'),


    path('message/', views.message, name='message'),
    path('delete_message/<int:m_id>/', views.delete_message, name='delete_message'),


]