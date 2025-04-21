from django.db import models
from django.contrib.auth.models import AbstractUser
from employees.managers import CustomUserManager

# Create your models here.



class Department(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(blank=True, null=True, verbose_name="Описание департамента")

    class Meta:
        verbose_name = "Отдел"
        verbose_name_plural = "Отделы"
        ordering = ["id"]

    def __str__(self):
            if self.name:
                return f"Отдел {self.name}"
            return f"Отдел {self.id}"

class Position(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название должности")
    salary = models.PositiveBigIntegerField(default=0, verbose_name="Оклад")

    class Meta:
        verbose_name = "Должность"
        verbose_name_plural = "Должности"
        ordering = ["id"]

    def __str__(self):
            if self.title:
                return f"Должность {self.title}"
            return f"Должность {self.id}"


class Employee(AbstractUser):
    fullname = models.CharField(max_length=128,verbose_name="Полное имя")
    email = models.EmailField(verbose_name="Электронная почта", unique=True)
    phone = models.CharField(max_length=20, verbose_name="Номер телефона")
    position = models.ForeignKey(Position, on_delete=models.SET_NULL,null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL,null=True, blank=True)
    hire_date = models.DateField(verbose_name="Дата найма",null=True,blank=True)
    photo = models.ImageField(upload_to='employees/', blank=True, null=True)
    is_head = models.BooleanField(verbose_name="Глава департамента", default=False)
    is_working = models.BooleanField(verbose_name="Работает", default=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"
        ordering = ["fullname"]

    def __str__(self):
        if self.fullname:
            return f"Сотрудник {self.fullname}"
        return f"Сотрудник {self.email}"