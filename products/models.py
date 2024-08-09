from django.db import models

# Create your models here.
class Product(models.Model):
    ProductName = models.CharField(max_length=100)

    def __str__(self):
        return self.ProductName
    