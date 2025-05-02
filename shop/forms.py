from django import forms
from .models import CompanyInfo, FoodItem, Order

class CompanyInfoForm(forms.ModelForm):
    class Meta:
        model = CompanyInfo
        fields = '__all__'
class FoodItemForm(forms.ModelForm):
    class Meta:
        model = FoodItem
        fields = '__all__'

class OrderStatusForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

