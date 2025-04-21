from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import auth_logout

from django.views.generic import CreateView, View, TemplateView, ListView
from django.urls import reverse_lazy
from employees.models import Employee
from employees.forms import EmployeeRegistrationForm
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotFound,HttpResponseForbidden


class EmployeeLoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True  
    next_page = reverse_lazy("dashboard")
       
    

class EmployeeLogoutView(View):
    def post(self, request, *args, **kwargs):
        auth_logout(request)
        return HttpResponseRedirect(reverse_lazy("login"))
    def get(self, request, *args, **kwargs):
        auth_logout(request)
        return HttpResponseRedirect(reverse_lazy("login"))
    

class Profile(View):
    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            employee = self.request.user
            if employee.is_head or employee.is_superuser:
                print("НАЧАЛЬНИК")
            else:
                print("СОТРУДНИК")
            return HttpResponse("ok")
        else:
            return HttpResponseNotFound()
        
class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_head'] = self.request.user.is_head
        return context
    

class EmployeeListView(LoginRequiredMixin, ListView):
    model = Employee
    template_name = 'employee_list.html'
    context_object_name = 'employees'
        
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Employee.objects.exclude(id=user.id)
        department = user.department
        return Employee.objects.filter(department=department).exclude(id=user.id)