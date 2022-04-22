from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from .models import Order, Customer #từ thư mục models, import đối tượng Order

class CustomerForm(ModelForm):
    class Meta: 
        model = Customer
        fields = '__all__'
        exclude = ['user']

class OrderForm(ModelForm):
    class Meta:
        model = Order # chỉ ra model mình sẽ build form
        fields = '__all__' # something likes customer, product .... thats all of them


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']