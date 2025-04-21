from django.contrib import admin, auth
from employees.models import Position,Department,Employee
# Register your models here.


admin.site.register(Employee)
admin.site.register(Department)
admin.site.register(Position)
admin.site.unregister(auth.models.Group)