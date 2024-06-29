from dataclasses import fields
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from inventory.models import Product, Order
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class UserRegistry(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name','email', 'password1', 'password2']


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'quantity', 'description','price']

        
    
    def save(self, commit=True):
        name = self.cleaned_data['name']
        price = self.cleaned_data['price']
        quantity = self.cleaned_data['quantity']

    
        existing_product = Product.objects.filter(name=name).first()

        if existing_product:
            if existing_product.price == price:
                
                existing_product.quantity += quantity
                if commit:
                    existing_product.save()
                return existing_product
            else:
                
                return super(ProductForm, self).save(commit=commit)
        else:
            
            return super(ProductForm, self).save(commit=commit)
        
    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Save'))

    
        self.fields['price'].widget.attrs['placeholder'] = 'Enter price per piece or unit' 
    

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['product', 'order_quantity','seller']

class EditProductForm(forms.Form):
    product_choice = forms.ModelChoiceField(queryset=Product.objects.all(), empty_label="Select Product to Edit")
    quantity = forms.IntegerField(min_value=1)
    price = forms.DecimalField(min_value=0.01, max_digits=10, decimal_places=2)
    description = forms.CharField(max_length=200, required=False)