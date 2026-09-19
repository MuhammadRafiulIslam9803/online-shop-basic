from django.db import models


# Create your models here.

CATEGORY_CHOICES = [
    ("shirt", "Shirt"),
    ("pant", "Pant"),
    ("borka", "Borka"),
    ("kids", "Kids"),
    ("shoes", "Shoes"),
]


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discounted_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    image = models.ImageField(upload_to="productImages/")
    description = models.TextField()
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)

    def __str__(self):
        return self.name
