# views.py
from django.views.generic import ListView, CreateView
from orders.models import Vacation, SickLeave
from employees.models import Employee
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden


class VacationListView(LoginRequiredMixin, ListView):
    model = Vacation
    template_name = 'vacation_list.html'
    context_object_name = 'vacations'
   
    
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Vacation.objects.exclude(employee__id=user.id)
        department = user.department
        return Vacation.objects.filter(employee__department=department)

class SickLeaveListView(LoginRequiredMixin, ListView):
    model = SickLeave
    template_name = 'sickleave_list.html'
    context_object_name = 'sick_leaves'
        
    
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return SickLeave.objects.exclude(employee__id=user.id)
        department = user.department
        return SickLeave.objects.filter(employee__department=department)