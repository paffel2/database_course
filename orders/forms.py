# forms.py
from django import forms
from orders.models import Order, SickLeave,Vacation
from employees.models import Employee, Position,Department

class DismissalOrderForm(forms.ModelForm):
    employee = forms.ModelChoiceField(
        queryset=Employee.objects.filter(is_active=True),
        label="Сотрудник"
    )
    
    class Meta:
        model = Order
        fields = ['employee', 'number',  'basis', "order_type"]
        widgets = {
            'basis': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'number': 'Номер приказа',
            'basis': 'Основание',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['order_type'].initial = 'dismiss'
        self.fields['order_type'].widget = forms.HiddenInput()


class VacationOrderForm(forms.ModelForm):
    order_number = forms.CharField(label="Номер приказа")
    basis = forms.CharField(label="Основание", widget=forms.Textarea(attrs={'rows': 3}))
    
    class Meta:
        model = Vacation
        fields = ['employee', 'start_date', 'end_date', 'vacation_type',"is_paid"]
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get('start_date')
        end = cleaned_data.get('end_date')
        
        if start and end and start > end:
            raise forms.ValidationError("Дата начала отпуска должна быть раньше даты окончания")
        
        return cleaned_data
    

class SickLeaveOrderForm(forms.ModelForm):
    order_number = forms.CharField(label="Номер приказа")
    basis = forms.CharField(label="Основание", widget=forms.Textarea(attrs={'rows': 3}))
    
    class Meta:
        model = SickLeave
        fields = ['employee', 'start_date', 'end_date', "sick_number"]
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get('start_date')
        end = cleaned_data.get('end_date')
        
        if start and end and start > end:
            raise forms.ValidationError("Дата начала больничного должна быть раньше даты окончания")
        
        return cleaned_data
    

class HireOrderForm(forms.ModelForm):
    email = forms.EmailField(label="Email (логин)")
    fullname = forms.CharField(label="Полное имя")
    phone = forms.CharField(label="Телефон")
    position = forms.ModelChoiceField(
        queryset=Position.objects.all(),
        label="Должность"
    )
    department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        label="Отдел")
    
    class Meta:
        model = Order
        fields = ['number',  'basis']
        widgets = {
            'basis': forms.Textarea(attrs={'rows': 3}),
        }