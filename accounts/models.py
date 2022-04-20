from django.db import models

# Create your models here.
class Customer(models.Model): # để thêm customer vào db thì cần chạy lệnh makemigrations (python manage.py makemigrations)
								#chỉ là bước đầu, để hoàn thiện quá trình thêm vào db cần chạy python manage.py migrate
	name = models.CharField(max_length=200, null=True) #cho phep gia tri null
	phone = models.CharField(max_length=200,null=True)
	email = models.CharField(max_length=200,null=True)
	date_created = models.DateTimeField(auto_now_add = True,null=True)

	def __str__(self):  #hiện tên của object customer trên admin panel
		return self.name

class Tag(models.Model): 
	name = models.CharField(max_length=200, null=True) #cho phep gia tri null

	def __str__(self):  #hiện tên của object customer trên admin panel
		return self.name

class Product(models.Model):
	CATEGORY = (
			('Indoor','Indoor'),
			('Outdoor','Outdoor'),
			)
	name= models.CharField(max_length=200, null=True)
	price = models.FloatField(null=True)
	category = models.CharField(max_length=200, null=True, choices=CATEGORY) #category xac dinh gia tri dua vao CATEGORY, like a dropdown menu
	discription = models.CharField(max_length=200, null=True, blank=True)
	date_created = models.DateTimeField(auto_now_add = True,null=True)
	tags = models.ManyToManyField(Tag)

	def __str__(self):  #hiện tên của object customer trên admin panel
		return self.name


class Order(models.Model):
	STATUS = (
			('Pending','Pending'),
			('Out for delivery','Out for delivery'),
			('Delivered','Delivered'),
			)
	customer = models.ForeignKey(Customer, null=True, on_delete = models.SET_NULL)  # set khóa ngoại trỏ tới bảng Customer
																# on_delete: khi xóa 1 customer trong bảng cus nhưng có 
																			#khóa ngoại tới bảng order, thì giá trị cus trong order = null
	product = models.ForeignKey(Product, null=True, on_delete = models.SET_NULL) 
	date_created = models.DateTimeField(auto_now_add = True,null=True)
	status = models.CharField(max_length=200, null=True, choices=STATUS)
