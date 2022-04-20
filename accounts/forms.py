from django.forms import ModelForm
from .models import Order #từ thư mục models, import đối tượng Order


class OrderForm(ModelForm):
    class Meta:
        model = Order # chỉ ra model mình sẽ build form
        fields = '__all__' # something likes customer, product .... thats all of them