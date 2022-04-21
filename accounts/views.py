from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory   #create multiple forms within 1 form
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group

from django.contrib.auth.decorators import login_required
# Create your views here.
from .models import *
from .forms import OrderForm, CreateUserForm
from .filters import OrderFilter 
from .decorators import unauthenticated_user, admin_only


# kiwine - midterm2022
#demo9 - final1234
@unauthenticated_user
def registerPage(request):
	if request.user.is_authenticated:
		return redirect('home')
	else:
		form = CreateUserForm()

		if request.method == 'POST':
			form = CreateUserForm(request.POST)
			if form.is_valid():
				user = form.save()
				username = form.cleaned_data.get('username') #get username and not get any atts
				
				group = Group.objects.get(name='customer')

				user.groups.add(group)

				messages.success(request, 'Account was created for ' + user)
				return redirect('login')

		context = {'form':form}

		return render(request,'accounts/register.html',context)

@unauthenticated_user #if user is authenticated thi se chuyen den home, neu k thif se chay trang login
def loginPage(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(request,username=username, password=password)

		if user is not None:
			login(request, user)
			return redirect('home')
		else:
			messages.info(request, 'Username or Password is incorrect!!!') 

	context = {}
	return render(request,'accounts/login.html',context)

def logoutUser(request):
	logout(request)
	return redirect('login')


def userPage(request):
	context ={}
	return render(request,'accounts/user.html',context)


@login_required(login_url='login') #dđặt trước những view muốn hạn chế truy cập, thay vào đó sẽ đi đến trang login
@admin_only #chi nhung user co role la admin thi moic co quyen truy cap vao home
def home(request):
	orders = Order.objects.all()
	customers = Customer.objects.all()

	total_customers = customers.count()
	total_orders = orders.count()
	delivered = orders.filter(status='Delivered').count()
	pending = orders.filter(status ='Pending').count()

	context = {'orders':orders,'customers':customers, 'total_customers':total_customers,
				'total_orders':total_orders,'delivered':delivered, 'pending':pending }
	return render(request,'accounts/dashboard.html',context) #render tới vị trí file dashboard.html

@login_required(login_url='login')
@admin_only #chi nhung user co role la admin thi moic co quyen truy cap vao home
def products(request):
	products = Product.objects.all() #truyen tham so dau vao
	return render(request,'accounts/products.html',{'products':products})

@login_required(login_url='login')
@admin_only #chi nhung user co role la admin thi moic co quyen truy cap vao home
def customer(request, pk_test):
	customer = Customer.objects.get(id=pk_test)
	orders = customer.order_set.all()
	order_count = orders.count()

	myFilter = OrderFilter(request.GET, queryset=orders)  #request.get send request data to this view
														#query tất cả order

	orders = myFilter.qs  #orders từ filter trả về 
	context = {'customer':customer,'orders':orders,'order_count':order_count,'myFilter':myFilter}
	return render(request,'accounts/customer.html',context)

@login_required(login_url='login')
@admin_only #chi nhung user co role la admin thi moic co quyen truy cap vao home
def createOrder(request, pk):
	OrderFormSet = inlineformset_factory(Customer, Order, fields=('product','status'), extra=10) #extra=10 means create 10 forms in formset 
	customer = Customer.objects.get(id=pk)
	formset = OrderFormSet(queryset = Order.objects.none(),instance=customer) #queyset likes that to hide existed orders of customer
	#form = OrderForm(initial={'customer':customer})
	if request.method == "POST":
		#print('Printing POST: ', request.POST)
		formset = OrderFormSet(request.POST, instance=customer)
		if formset.is_valid(): #nếu form is valid thì save thông tin xuống db
			formset.save()
			return redirect('/') # save infomation into db, then back to home view and show new info
	context = {'formset':formset}
	return render(request,'accounts/order_form.html',context)

@login_required(login_url='login')
@admin_only #chi nhung user co role la admin thi moic co quyen truy cap vao home
def updateOrder(request, pk):
	order = Order.objects.get(id=pk)
	form = OrderForm(instance=order)
	if request.method == "POST":	
		form = OrderForm(request.POST, instance=order)  #thay vi create new item, thì sẽ lấy dữ liệu từ instance truyền vào
		if form.is_valid(): 
			form.save()
			return redirect('/')  
	context = {'form':form}

	return render(request,'accounts/order_form.html',context)

@login_required(login_url='login')
@admin_only #chi nhung user co role la admin thi moic co quyen truy cap vao home
def deleteOrder(request, pk):
	order = Order.objects.get(id=pk)
	if request.method=="POST":
		order.delete()
		return redirect('/')

	context ={'item':order}

	return render(request,'accounts/delete.html',context)
	
