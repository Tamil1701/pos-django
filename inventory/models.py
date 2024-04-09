import random
from email.policy import default
from django.db import models
from django.contrib.auth.models import User

CATEGORY = (
    ('Stationary', 'Stationary'),
    ('Electronics', 'Electronics'),
    ('Food', 'Food')
)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    physical_address = models.CharField(max_length=40, null=True)
    mobile = models.CharField(max_length=12, null=True)
    picture = models.ImageField(default='avatar.jpeg' ,upload_to='Pictures')

    def __str__(self) -> str:
        return self.user.username


class Product(models.Model):
    name = models.CharField(max_length=100, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY, null=True)
    quantity = models.PositiveIntegerField(null=True)
    description = models.CharField(max_length=200, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
        return str(self.item) + ": $" + str(self.price)

    def __str__(self) -> str:
        return self.name


class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ]

    INVOICE_STATUS_CHOICES = [
        ('not_generated', 'Not Generated'),
        ('generated', 'Generated'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    order_quantity = models.PositiveIntegerField(null=True)
    date = models.DateTimeField(auto_now_add=True)
    seller_choices = [
        ('seller1', 'Seller 1 - Address 1'),
        ('seller2', 'Seller 2 - Address 2'),
        ('seller3', 'Seller 3 - Address 3'),
    ]
    seller = models.CharField(max_length=10, choices=seller_choices, default='seller1')
    order_status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='pending')
    invoice_status = models.CharField(max_length=20, choices=INVOICE_STATUS_CHOICES, default='not_generated')
    order_id = models.CharField(max_length=4, unique=True)

    def __str__(self) -> str:
        return f'{self.product} ordered quantity {self.order_quantity} from {self.get_seller_display()}'

    def save(self, *args, **kwargs):
        if not self.order_id:
            self.order_id = self.generate_order_id()
        super().save(*args, **kwargs)

    def generate_order_id(self):
        # Generate a random 4-digit order ID
        return str(random.randint(1000, 9999))