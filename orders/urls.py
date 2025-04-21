from django.urls import path
from orders.views import VacationListView,SickLeaveListView

urlpatterns = [
    path('vacations/', VacationListView.as_view(), name='vacations'),
    path('sickleaves/', SickLeaveListView.as_view(), name='sickleaves'),
  #  path('profile/', Profile.as_view(), name='profile'),
   # path('dashboard/', DashboardView.as_view(), name='dashboard'),
]