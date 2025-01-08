from django import forms
from .models import Promotion
from customer.models import Customer

class PromotionForm(forms.ModelForm):
    customers = forms.ModelMultipleChoiceField(
        queryset=Customer.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    select_all = forms.BooleanField(required=False, label='Select All Active Customers', widget=forms.CheckboxInput(attrs={'id': 'select-all'}))

    class Meta:
        model = Promotion
        fields = ['title', 'description', 'start_date', 'end_date', 'active', 'customers', 'select_all']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'customers': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['customers'].queryset = Customer.objects.filter(active=True)

        if user and user.role != 'admin':
            self.fields.pop('active')