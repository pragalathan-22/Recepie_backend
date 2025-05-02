from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Order
import datetime

@receiver(pre_save, sender=Order)
def generate_order_number(sender, instance, **kwargs):
    if not instance.order_number:
        # Generate order number in format: ORD-YYYYMMDD-XXXX
        today = datetime.datetime.now()
        last_order = Order.objects.filter(
            created_at__date=today.date()
        ).order_by('-order_number').first()
        
        if last_order:
            last_number = int(last_order.order_number.split('-')[-1])
            new_number = last_number + 1
        else:
            new_number = 1
            
        instance.order_number = f"ORD-{today.strftime('%Y%m%d')}-{new_number:04d}" 