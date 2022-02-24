from django.contrib import admin
from .models import register, product,Category,order
# Register your models here.



admin.site.register(register)
admin.site.register(product)
admin.site.register(Category)
admin.site.register(order)


