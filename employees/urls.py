from django.urls import path
from employees.views import EmployeeLoginView, EmployeeLogoutView,Profile, DashboardView,EmployeeListView

urlpatterns = [
    path('login/', EmployeeLoginView.as_view(), name='login'),
    path('logout/', EmployeeLogoutView.as_view(), name='logout'),
    path('profile/', Profile.as_view(), name='profile'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('employees/', EmployeeListView.as_view(), name='employee_list'),
]