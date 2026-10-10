from django.db import models
from django.contrib.auth.models import User


# Create your models here.

# for my product information

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


DISTRICT_CHOICES = [
    ("Dhaka", "Dhaka"),
    ("Chittagong", "Chittagong"),
    ("Khulna", "Khulna"),
    ("Rajshahi", "Rajshahi"),
    ("Barisal", "Barisal"),
    ("Sylhet", "Sylhet"),
    ("Rangpur", "Rangpur"),
    ("Mymensingh", "Mymensingh"),
]


# for customer information as profile
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    district = models.CharField(choices=DISTRICT_CHOICES, max_length=100)
    thana = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=10)
    phone = models.CharField(max_length=15)
    village = models.CharField(max_length=100)

    def __str__(self):
        return str(self.id)


# for cart and order information
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cart")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Cart"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["cart", "product"], name="unique_product_per_cart"
            )
        ]

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"

# for placement of order
class Order(models.Model):

    ORDER_STATUS = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("processing", "Processing"),
        ("shipped", "Shipped"),
        ("delivered", "Delivered"),
        ("cancelled", "Cancelled"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="orders"
    )

    customer = models.ForeignKey(
        Customer,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    # Product total before shipping
    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    # Delivery charge
    shipping_charge = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    # subtotal + shipping_charge
    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    status = models.CharField(
        max_length=20,
        choices=ORDER_STATUS,
        default="pending"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"


class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items"
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    quantity = models.PositiveIntegerField()

    # Product price at the time of ordering
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    # price × quantity
    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def __str__(self):
        return f"{self.product} x {self.quantity}"