from django.contrib import admin
from orders.models import Order,Vacation,SickLeave
# Register your models here.


admin.site.register(Order)
admin.site.register(Vacation)
admin.site.register(SickLeave)
