import os
from django.db import models
from products.models import Product
from django.core.validators import RegexValidator
from django.utils import timezone

def generate_order_id():
    return f"{timezone.now().strftime('%Y%m%d')}{Order.objects.count() + 1:04d}"

class Order(models.Model):
    ordered_date = models.DateTimeField(auto_now_add=True)
    order_time = models.TimeField(auto_now_add=True)
    order_id = models.CharField(max_length=14, primary_key=True, default=generate_order_id)
    printer_name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    contact_number = models.CharField(
        max_length=10,
        validators=[
            RegexValidator(
                regex='^[1-9][0-9]{9}$',
                message='Contact number must be a 10 digit number without leading zeros',
            ),
        ]
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    front_side_image = models.ImageField(upload_to='order_images')
    back_side_image = models.ImageField(upload_to='order_images',blank=True, null=True)
    front_side_image_url = models.URLField(blank=True, null=True)
    back_side_image_url = models.URLField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.order_id:
            self.order_id = generate_order_id()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.order_id} - {self.printer_name}"
