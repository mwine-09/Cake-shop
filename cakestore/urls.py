from django.urls import path
from . import views
from  django.contrib.auth import views as auth_views


urlpatterns = [
    path('login_user/', views.login_user, name="login"),
    path('logout_user/', views.logout_user, name='logout'),
    path('register_user/', views.register_user, name='register'),
    path('profile/', views.profile, name='profile'),
    path('about/', views.showAbout, name = 'about'),
    path('payment/', views.showPayment, name ='payment'),
    path('menu/', views.showMenu, name = 'menu'),
    path('', views.showHome, name = 'home'),
    path('menu/<category>/', views.menuByCategory, name = 'menuByCategory'),
    path('addCart/<str:id>/', views.addCart, name='addCart'),
    path('Cart/',views.display, name= 'Cart'),
    path('checkout/',views.checkout, name= 'checkout'),
    path('payments/',views.payments, name= 'payments'),

    path('add/<int:id>/',views.add, name= 'add'),
    path('reduce/<int:id>/',views.reduce, name='reduce'),

    path('search_item/',views.search_item, name='search_item'),
    path('delete/<str:id>/',views.delete_from_cart, name='delete_from_cart'),
    path('charge/', views.charge, name="charge"),
    # path('reset-password/', views.reset_password, name="password_reset"),
    path('reset-password/', auth_views.PasswordResetView.as_view(), name="password_reset"),
    path('orders/',views.show_orders, name="orders"),
    path('cod/',views.cash_on_delivery, name='cash_on_delivery'),






]

