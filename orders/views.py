from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from orders.models import Vacation, SickLeave, Order
from orders.forms import (
    DismissalOrderForm,
    VacationOrderForm,
    SickLeaveOrderForm,
    HireOrderForm,
    UpdateVacationOrderForm,
    UpdateSickLeaveOrderForm,
)
from employees.models import Employee
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.contrib.auth.hashers import make_password
import random
import string
from orders.tasks import send_email
from django.contrib import messages


class VacationListView(LoginRequiredMixin, ListView):
    model = Vacation
    template_name = "vacation_list.html"
    context_object_name = "vacations"

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Vacation.objects.exclude(employee__id=user.id)
        department = user.department
        return Vacation.objects.filter(employee__department=department)


class SickLeaveListView(LoginRequiredMixin, ListView):
    model = SickLeave
    template_name = "sickleave_list.html"
    context_object_name = "sick_leaves"

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return SickLeave.objects.exclude(employee__id=user.id)
        department = user.department
        return SickLeave.objects.filter(employee__department=department)


class CreateDismissalOrderView(LoginRequiredMixin, CreateView):
    model = Order
    form_class = DismissalOrderForm
    template_name = "create_dismissal.html"
    success_url = reverse_lazy("orders_list")

    def form_valid(self, form):
        form.instance.order_type = "dismiss"
        form.instance.employee = self.request.user
        dismissed = form.cleaned_data["employee"]
        dismissed.is_active = False
        dismissed.save()
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_head or request.user.is_superuser):
            return HttpResponseForbidden("Только руководители могут создавать приказы")
        return super().dispatch(request, *args, **kwargs)


class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = "orders_list.html"
    context_object_name = "orders"
    ordering = ["-date"]
    paginate_by = 20

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        if user.is_superuser:
            queryset = queryset
        else:
            department = user.department
            queryset = queryset.filter(employee__department=department)
        order_type = self.request.GET.get("type")
        if order_type:
            queryset = queryset.filter(order_type=order_type)
        return queryset


class CreateVacationOrderView(LoginRequiredMixin, CreateView):
    form_class = VacationOrderForm
    template_name = "create_vacation.html"
    success_url = reverse_lazy("vacations")

    def form_valid(self, form):
        vacation = form.save(commit=False)
        vacation.order_number = form.cleaned_data["order_number"]
        vacation.save()
        current_user = self.request.user
        order = Order.objects.create(
            number=form.cleaned_data["order_number"],
            order_type="vacation",
            employee=current_user,
            basis=form.cleaned_data["basis"],
        )
        order.refresh_from_db()
        vacation.order = order
        vacation.save()

        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_head or request.user.is_superuser):
            return HttpResponseForbidden("Только руководители могут создавать приказы")
        return super().dispatch(request, *args, **kwargs)


class CreateSickLeaveOrderView(LoginRequiredMixin, CreateView):
    form_class = SickLeaveOrderForm
    template_name = "create_sickleave.html"
    success_url = reverse_lazy("sickleaves")

    def form_valid(self, form):
        sickleave = form.save(commit=False)
        sickleave.order_number = form.cleaned_data["order_number"]
        sickleave.save()
        current_user = self.request.user
        order = Order.objects.create(
            number=form.cleaned_data["order_number"],
            order_type="vacation",
            employee=current_user,
            basis=form.cleaned_data["basis"],
        )

        order.refresh_from_db()
        sickleave.order = order
        sickleave.save()
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_head or request.user.is_superuser):
            return HttpResponseForbidden("Только руководители могут создавать приказы")
        return super().dispatch(request, *args, **kwargs)


class CreateHireOrderView(LoginRequiredMixin, CreateView):
    form_class = HireOrderForm
    template_name = "create_hire.html"
    success_url = reverse_lazy("orders_list")

    def form_valid(self, form):
        alphabet = string.ascii_letters + string.digits
        password = "".join(random.choices(alphabet, k=12))

        employee = Employee.objects.create(
            username=form.cleaned_data["email"],
            email=form.cleaned_data["email"],
            fullname=form.cleaned_data["fullname"],
            phone=form.cleaned_data["phone"],
            position=form.cleaned_data["position"],
            department=form.cleaned_data["department"],
            password=make_password(password),
            is_active=True,
        )

        order = form.save(commit=False)
        order.order_type = "hire"
        current_user = self.request.user
        order.employee = current_user
        order.save()

        ctx = {"email": employee.email, "password": password}
        print(ctx)
        # send_email.apply_async(
        #     ["Новый сотрудник", "create_email.html", ctx, employee.email]
        # )

        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_head or request.user.is_superuser):
            return HttpResponseForbidden("Только руководители могут создавать приказы")
        return super().dispatch(request, *args, **kwargs)


class UpdateVacationOrderView(LoginRequiredMixin, UpdateView):
    model = Vacation
    form_class = UpdateVacationOrderForm
    template_name = "update_vacation.html"
    context_object_name = "vacation"
    success_url = reverse_lazy("vacations")

    def form_valid(self, form):
        messages.success(self.request, "Отпуск успешно обновлен")
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_head or request.user.is_superuser):
            return HttpResponseForbidden(
                "Только руководители могут редактировать отпуска"
            )
        return super().dispatch(request, *args, **kwargs)


class UpdateSickLeaveOrderView(LoginRequiredMixin, UpdateView):
    model = SickLeave
    form_class = UpdateSickLeaveOrderForm
    template_name = "update_sickleave.html"
    context_object_name = "sickleave"
    success_url = reverse_lazy("sickleaves")

    def form_valid(self, form):
        messages.success(self.request, "Больничный успешно обновлен")
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_head or request.user.is_superuser):
            return HttpResponseForbidden(
                "Только руководители могут редактировать больничные"
            )
        return super().dispatch(request, *args, **kwargs)
