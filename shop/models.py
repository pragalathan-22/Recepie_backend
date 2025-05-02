from django.db import models
from django.utils import timezone

class CompanyInfo(models.Model):
    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='logos/')

    def __str__(self):
        return self.name

class FoodItem(models.Model):
    CATEGORY_CHOICES = [
        ('top', 'Top Rated'),
        # ('recommended', 'Recommended'),
        ('all', 'All Foods'),
    ]

    name = models.CharField(max_length=255,blank=True,null=True)
    rate = models.DecimalField(max_digits=6, decimal_places=2,blank=True,null=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    subcategory = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to='foods/',blank=True,null=True)
    # video = models.FileField(upload_to='foods/videos/', blank=True, null=True)
    
    def __str__(self):
        return f"{self.name} - {self.category} - {self.subcategory or 'No Sub'}"

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    order_number = models.CharField(max_length=20, unique=True)
    customer_name = models.CharField(max_length=255)
    customer_phone = models.CharField(max_length=15)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Order #{self.order_number} - {self.customer_name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    
    def __str__(self):
        return f"{self.quantity}x {self.food_item.name} for Order #{self.order.order_number}"



class Transaction(models.Model):
    order_id = models.CharField(max_length=100)
    payment_id = models.CharField(max_length=100, blank=True, null=True)
    amount = models.FloatField()
    status = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction {self.order_id}"


class Advertisement(models.Model):
    title = models.CharField(max_length=255)
    video = models.FileField(upload_to='advertisements/videos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title



        