from dataclasses import fields
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from inventory.models import Product, Order

class UserRegistry(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name','is_staff','is_superuser', 'email', 'password1', 'password2']


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'quantity', 'description','price']


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['product', 'order_quantity','seller']

class EditProductForm(forms.Form):
    product_choice = forms.ModelChoiceField(queryset=Product.objects.all(), empty_label="Select Product to Edit")
    quantity = forms.IntegerField(min_value=1)
    price = forms.DecimalField(min_value=0.01, max_digits=10, decimal_places=2)
    description = forms.CharField(max_length=200, required=False)