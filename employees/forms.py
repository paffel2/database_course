from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from employees.models import Employee
from django import forms


class EmployeeRegistrationForm(UserCreationForm):
    class Meta:
        model = Employee
        fields = [
            "email",
            "fullname",
            "password1",
            "password2",
            "position",
            "department",
            "phone",
        ]


def LoginForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        if user.is_staff and not user.is_superuser:
            raise forms.ValidationError(
                ("This account is not allowed here."),
                code="not_allowed",
            )
        if not user.is_working:
            raise forms.ValidationError(
                ("This account is not allowed here."),
                code="not_allowed",
            )
