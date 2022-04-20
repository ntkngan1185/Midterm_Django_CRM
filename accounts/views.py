from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory   #create multiple forms within 1 form
# Create your views here.
from .models import *
from .forms import OrderForm
from .filters import OrderFilter 

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

def products(request):
	products = Product.objects.all() #truyen tham so dau vao
	return render(request,'accounts/products.html',{'products':products})

def customer(request, pk_test):
	customer = Customer.objects.get(id=pk_test)
	orders = customer.order_set.all()
	order_count = orders.count()

	myFilter = OrderFilter(request.GET, queryset=orders)  #request.get send request data to this view
														#query tất cả order

	orders = myFilter.qs  #orders từ filter trả về 
	context = {'customer':customer,'orders':orders,'order_count':order_count,'myFilter':myFilter}
	return render(request,'accounts/customer.html',context)
 
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

def deleteOrder(request, pk):
	order = Order.objects.get(id=pk)
	if request.method=="POST":
		order.delete()
		return redirect('/')

	context ={'item':order}

	return render(request,'accounts/delete.html',context)
	
