from django.db import models
from employees.models import Employee

class Order(models.Model):
    ORDER_TYPES = [
        ('hire', 'Прием на работу'),
        ('dismiss', 'Увольнение'),
        ('vacation', 'Отпуск'),
    ]
    number = models.CharField(max_length=50, verbose_name="Номер приказа")
    order_type = models.CharField(max_length=50, choices=ORDER_TYPES,verbose_name="Тип приказа")
    date = models.DateField(auto_now_add=True, verbose_name="Дата издания приказа")
    script_data = models.DateField(verbose_name="Дата подписания",null=True,blank=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name="Сотрудник")
    basis = models.TextField(null=True,blank=True, verbose_name="Основание")


    class Meta:
        verbose_name = "Приказ"
        verbose_name_plural = "Приказы"
        ordering = ["number"]

    def __str__(self):
        if self.fullname:
            return f"Приказ {self.number}"
        return f"Приказ {self.id}"

class Vacation(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE,verbose_name="Сотрудник")
    start_date = models.DateField(verbose_name="Дата начала",null=True,blank=True)
    end_date = models.DateField(verbose_name="Дата окончания",null=True,blank=True)
    vacation_type = models.CharField(max_length=50, verbose_name="Комментарий")
    is_paid = models.BooleanField(default=True, verbose_name="Оплачиваемый отпуск")

    class Meta:
        verbose_name = "Отпуск"
        verbose_name_plural = "Отпуска"
        ordering = ["id"]


class SickLeave(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE,verbose_name="Сотрудник")
    start_date = models.DateField(verbose_name="Дата начала",null=True,blank=True)
    end_date = models.DateField(verbose_name="Дата окончания",null=True,blank=True)
    sick_number = models.CharField(max_length=50, verbose_name="Номер больничного листа")

    class Meta:
        verbose_name = "Больничный"
        verbose_name_plural = "Больничные"
        ordering = ["id"]