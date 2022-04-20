from django.contrib import admin

# Register your models here.

from .models import * #để table vừa tạo có thể hiện trên panel admin thì cần đăng ký chúng tại đây
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
