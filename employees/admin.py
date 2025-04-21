from django.contrib import admin, auth
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from employees.models import Position,Department,Employee
# Register your models here.



class UserAdmin(BaseUserAdmin):
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
    fieldsets = (
        (
            "Главная информация",
            {
                "fields": (
                    "email",
                    "password",
                )
            },
        ),
        (
            "Личная информация",
            {"fields": ("fullname", "phone")},
        ),

        ("Статус", {"fields": ("is_staff", "is_superuser", "is_active","is_head")}),
        ("Департамент", {"fields":("department",)}),
        ("Должность", {"fields":("position",)})
    )
    list_display = ("id", "email", "phone", "is_superuser", "is_active")
    ordering = ["-id"]
    search_fields = ("email",)


admin.site.register(Employee,UserAdmin)
admin.site.register(Department)
admin.site.register(Position)
admin.site.unregister(auth.models.Group)