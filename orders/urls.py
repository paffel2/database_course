from django.urls import path
from orders.views import (
    VacationListView,
    SickLeaveListView,
    CreateDismissalOrderView,
    OrderListView,
    CreateVacationOrderView,
    CreateSickLeaveOrderView,
    CreateHireOrderView,
    UpdateVacationOrderView,
    UpdateSickLeaveOrderView,
)

urlpatterns = [
    path("vacations/", VacationListView.as_view(), name="vacations"),
    path("sickleaves/", SickLeaveListView.as_view(), name="sickleaves"),
    path("create_dismiss/", CreateDismissalOrderView.as_view(), name="create_dismiss"),
    path("orders_list/", OrderListView.as_view(), name="orders_list"),
    path("create_vacation/", CreateVacationOrderView.as_view(), name="create_vacation"),
    path(
        "create_sickleave/", CreateSickLeaveOrderView.as_view(), name="create_sickleave"
    ),
    path("create_employee/", CreateHireOrderView.as_view(), name="create_employee"),
    path(
        "vacations/update/<int:pk>/",
        UpdateVacationOrderView.as_view(),
        name="update_vacation",
    ),
    path(
        "sickleaves/update/<int:pk>/",
        UpdateSickLeaveOrderView.as_view(),
        name="update_sickleave",
    ),
]
