from django import forms
from .models import Order
from products.models import Product

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'printer_name', 'location', 'contact_number', 'product',
            'quantity', 'front_side_image', 'back_side_image', 'email'
        ]
        help_texts = {
            'email': 'If you provide an email address, a link to the order details will be sent to your email.',
        }

    def clean_contact_number(self):
        contact_number = self.cleaned_data.get('contact_number')
        if not contact_number.isdigit():
            raise forms.ValidationError("Contact number must contain only digits.")
        if len(contact_number) != 10:
            raise forms.ValidationError("Contact number must be a 10-digit number.")
        return contact_number

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].queryset = Product.objects.all()

    def save(self, commit=True):
        print('Entered OrderForm save method')
        instance = super(OrderForm, self).save(commit=False)
        print(f'Instance to save: {instance}')
        if commit:
            instance.save()
            print(f'Instance saved with ID: {instance.order_id}')
        return instance
