from taggit.serializers import (TagListSerializerField,
                                TaggitSerializer)
from rest_framework import serializers

from store.models import Product, ProductPrice, ProductImage, Transaction, Order, Store, Customer

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('user', 'phone')


class ProductPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPrice
        fields = ('purchase_price', 'selling_price')


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('image', 'order')


class ProductSerializer(TaggitSerializer, serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    latest_selling_price = serializers.FloatField(read_only=True)
    tags = TagListSerializerField()
    class Meta:
        model = Product
        fields = ('id', 'title', 'description', 'tags', 'images', 'latest_selling_price')


class TransactionSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = Transaction
        fields = ('quantity', 'product', 'content_type', 'object_id')

    def validate_content_type(self, value):
        allowed_models = ['order', 'store']
        if value.model not in allowed_models:
            raise serializers.ValidationError(f"Content type must be one of {allowed_models}.")
        return value


class OrderSerializer(serializers.ModelSerializer):
    transactions = TransactionSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ('customer', 'transactions', 'total_price')

class StoreSerializer(serializers.ModelSerializer):
    transactions = TransactionSerializer(many=True, read_only=True)

    class Meta:
        model = Store
        fields = ('title', 'address', 'transactions')