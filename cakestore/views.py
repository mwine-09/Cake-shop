from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegisterUserForm
from .models import Item,Cart,Category, cartItem, Order, orderItem
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.template import loader
from django.urls import reverse
from django.db import models
from django.db.models import Sum
from django.views.generic.base import TemplateView 
import stripe
from django.conf import settings
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string

def showHome(request):
	cart = Cart.objects.all()
	item = Item.objects.all()
	quantity = Cart.objects.all().aggregate(Sum('quantity'))
	post_quantity = quantity['quantity__sum']
	context = { 'items': item, 'cart': cart , 'quantity': post_quantity }
	return render (request, 'cakestore/index.html', context)




def showAbout(request):
	quantity = Cart.objects.all().aggregate(Sum('quantity'))
	post_quantity = quantity['quantity__sum']
	context = { 'quantity': post_quantity }
	return render (request, 'cakestore/About.html', context)


def showMenu(request):
	item = Item.objects.all()
	cart = Cart.objects.all()
	quantity = Cart.objects.all().aggregate(Sum('quantity'))
	post_quantity = quantity['quantity__sum']
	categoryList = Category.objects.all()
	context = { 'items': item, 'categories': categoryList , 'cart': cart , 'quantity': post_quantity }
	return render (request, 'cakestore/menu.html', context)

def menuByCategory(request, category):
	category = Category.objects.get(name=category)
	items = Item.objects.filter(category=category)
	quantity = Cart.objects.all().aggregate(Sum('quantity'))
	post_quantity = quantity['quantity__sum']
	context = { 'items': items, 'quantity': post_quantity }
	return render (request, 'cakestore/menu.html', context) 


#add a cartItem to the cart
def addCart(request, id):
	item = Item.objects.get(id=id)
	if Cart.objects.filter(item=item).exists():
		cart= Cart.objects.filter(item=item).update(quantity=models.F('quantity')+1)
		# cart.save()
		
		return HttpResponseRedirect(reverse('menu'))
	else:
		cart = Cart.objects.create(item=item, quantity=1)
		cart.save()

		return HttpResponseRedirect(reverse('menu'))
    

def display (request):
	if Cart.objects.all().count() == 0:
		message= "Your cart is empty"
		context ={ 'message': message }
		template = loader.get_template('cakestore/cart.html')
		return render (request, 'cakestore/cart.html', context)
	else:
		quantity = Cart.objects.all().aggregate(Sum('quantity'))
		post_quantity = quantity['quantity__sum']
		total = Cart.objects.all().aggregate(Sum('total_ordering'))
		post_tot = total['total_ordering__sum']

		cart = Cart.objects.all()
		context = { 'cart': cart, 'total': post_tot , 'quantity': post_quantity }



		return render (request, 'cakestore/cart.html', context)



 

@login_required(login_url='login')
def checkout(request):
	template = loader.get_template('cakestore/payments.html')
	cart = Cart.objects.all()
	total = Cart.objects.all().aggregate(Sum('total_ordering'))
	quantity = Cart.objects.all().aggregate(Sum('quantity'))
	quantity_value = quantity['quantity__sum']
	post_tot = total['total_ordering__sum']

	context1 = { 'cart': cart, 'key': settings.STRIPE_PUBLISHABLE_KEY, 'total': post_tot , 'quantity': quantity_value }
	return HttpResponse(template.render(context1, request))


#cart management functions

def delete_from_cart(request, id):
	Cart.objects.filter(id=id).delete()
	return HttpResponseRedirect(reverse('Cart'))


def reduce(request, id):
	if Cart.objects.filter(id=id).exists() and Cart.objects.filter(quantity =1):
		Cart.objects.filter(id=id).delete()
		return HttpResponseRedirect(reverse('Cart'))
	elif Cart.objects.filter(id=id).exists() and Cart.objects.filter(quantity__gte = 2):
		Cart.objects.filter(id=id).update(quantity=models.F('quantity')-1)
		return HttpResponseRedirect(reverse('Cart'))

def add (request, id):
	if Cart.objects.filter(id=id).exists():
		Cart.objects.filter(id=id).update(quantity=models.F('quantity')+1)
		return HttpResponseRedirect(reverse('Cart'))


 



#user authentication functions
def login_user(request):
	page = 'login'
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			return redirect('home')
		else:
			messages.success(request, ("There Was An Error Logging In, Try Again..."))	
			return redirect('login')	


	else:
		return render(request, 'cakestore/login.html', {"page":page})

def logout_user(request):
	logout(request)
	messages.success(request, ("You Were Logged Out!"))
	return redirect('home')



def register_user(request):
	if request.method == "POST":
		form = RegisterUserForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(username=username, password=password)
			login(request, user)
			messages.success(request, ("Registration Successful!"))
			return redirect('home')
	else:
		form = RegisterUserForm()

	return render(request, 'cakestore/login.html', {'form':form,})





#functions for the payments api

class HomePageview(TemplateView):
    template_name = 'cakestore/payments.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['key'] = settings.STRIPE_PUBLISHABLE_KEY
        return context



def charge(request):
	total = Cart.objects.all().aggregate(Sum('total_ordering'))
	post_tot = total['total_ordering__sum']
	if request.method == 'POST':
		charge = stripe.charge.Create(
            amount= post_tot,
            currency='ugx',
            description ='Check Out Charge',
            source = request.POST['stripeToken']
        )
		return render(request, 'cakestore/charge.html')


def payments(request):
	total = Cart.objects.all().aggregate(Sum('total_ordering'))
	post_tot = total['total_ordering__sum']
	cart = Cart.objects.all()
	context = { 'cart': cart, 'total': post_tot }
	template = loader.get_template('cakestore/payments.html')
	return HttpResponse(template.render(context))

def showPayment(request):
	template = loader.get_template('cakestore/payments.html')
	return HttpResponse(template.render(template), request= request)

def search_item(request):
	if request.method == 'GET':
		search = request.GET.get('search-text')
		search_result = Item.objects.filter(name__icontains=search)
		if search_result:
			context = {'items': search_result, 'search': search}
			template = loader.get_template('cakestore/search.html')
			return HttpResponse(template.render(context))
		else:
			message = "No result found"
			context = {'message': message}
			template = loader.get_template('cakestore/search.html')
			return HttpResponse(template.render(context))



def profile(request):
	template = loader.get_template('cakestore/profile.html')
	return HttpResponse(template.render())
	 



#function for showing orders
def show_orders(request):
	orders = Order.objects.all()
	quantity = Cart.objects.all().aggregate(Sum('quantity'))
	post_quantity = quantity['quantity__sum']
	context = {'orders': orders, 'quantity': post_quantity}
	return render (request, 'cakestore/orders.html', context)


#function that creates an order from the cart and saves to the order table
def cash_on_delivery(request):
	send_mail(request)
	create_order(request)
	messages.success(request, ("Order Placed Successfully!"))
	return render(request, 'cakestore/menu.html')

def create_order(request):
	cart = Cart.objects.all()
	for item in cart:
		order_item = orderItem.objects.create(item=item.item, quantity=item.quantity)
		order = Order.objects.create(User=request.user, item=order_item.item, quantity=order_item.quantity, total_ordering=item.total_ordering)
		order.save()
	Cart.objects.all().delete()
	return HttpResponseRedirect(reverse('orders'))




def send_mail(request):
	total = Cart.objects.all().aggregate(Sum('total_ordering'))
	post_tot = total['total_ordering__sum']
	cart = Cart.objects.all()
	username = request.user.username
	quantity = Cart.objects.all().aggregate(Sum('quantity'))
	post_quantity = quantity['quantity__sum']
	context = {'total': post_tot, 'quantity': post_quantity, 'cart': cart, 'username': username}
	template = loader.get_template('cakestore/email.html')
	
	email = EmailMessage(
		'Oder Confirmation',
		template.render(context),
		settings.EMAIL_HOST_USER,

		# [request.user.email]
		[request.user.email]

	)
	email.fail_silently = False
	email.send()

	

 