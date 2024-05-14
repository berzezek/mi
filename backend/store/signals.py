from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Transaction, Order

@receiver(post_save, sender=Transaction)
def update_order_total_price_on_save(sender, instance, **kwargs):
    if instance.content_type.model == 'order':
        order = Order.objects.get(id=instance.object_id)
        order.update_total_price()

@receiver(post_delete, sender=Transaction)
def update_order_total_price_on_delete(sender, instance, **kwargs):
    if instance.content_type.model == 'order':
        order = Order.objects.get(id=instance.object_id)
        order.update_total_price()
