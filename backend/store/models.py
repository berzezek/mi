from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from taggit.managers import TaggableManager
from simple_history.models import HistoricalRecords


class Customer(models.Model):
    user = models.OneToOneField("auth.User", on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True, null=True)
    history = HistoricalRecords()


class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    tags = TaggableManager()
    history = HistoricalRecords()

    def latest_selling_price(self) -> float:
        latest_price = self.prices.order_by("-id").first()
        return latest_price.selling_price if latest_price else 0

    class Meta:
        ordering = ("-id",)


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(upload_to="products")
    order = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if self.product.images.count() >= 5:
            raise Exception("You can not add more than 5 images to the product")
        super().save(*args, **kwargs)


class ProductPrice(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="prices"
    )
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    history = HistoricalRecords()

    def save(self, *args, **kwargs):
        if self.purchase_price > self.selling_price:
            raise Exception("Selling price must be greater than purchase price")
        super().save(*args, **kwargs)


class Transaction(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="transactions"
    )
    quantity = models.IntegerField(default=0)
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, related_name="transactions"
    )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    history = HistoricalRecords()


class Order(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="orders"
    )
    transactions = GenericRelation(Transaction)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    history = HistoricalRecords()

    def update_total_price(self):
        self.total_price = sum(
            t.product.latest_selling_price() * t.quantity
            for t in self.transactions.all()
        )
        super().save()


class Store(models.Model):
    title = models.CharField(max_length=255)
    address = models.TextField()
    transactions = GenericRelation(Transaction)
    history = HistoricalRecords()
