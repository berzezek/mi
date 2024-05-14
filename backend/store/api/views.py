from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from .serializers import (
    CustomerSerializer,
    ProductSerializer,
    ProductPriceSerializer,
    ProductImageSerializer,
    TransactionSerializer,
    OrderSerializer,
    StoreSerializer,
)
from store.models import (
    Customer,
    Product,
    ProductPrice,
    ProductImage,
    Transaction,
    Order,
    Store,
)


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductPriceViewSet(viewsets.ModelViewSet):
    queryset = ProductPrice.objects.all()
    serializer_class = ProductPriceSerializer

    def get_queryset(self):
        return super().get_queryset().filter(product_id=self.kwargs.get("product_id"))

    def perform_create(self, serializer):
        product = get_object_or_404(Product, id=self.kwargs.get("product_id"))
        serializer.save(product=product)


class ProductImageViewSet(viewsets.ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer

    def get_queryset(self):
        return super().get_queryset().filter(product_id=self.kwargs.get("product_id"))

    def perform_create(self, serializer):
        product = get_object_or_404(Product, id=self.kwargs.get("product_id"))
        serializer.save(product=product)


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class StoreViewSet(viewsets.ModelViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
