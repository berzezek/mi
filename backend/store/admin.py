from adminsortable2.admin import SortableAdminMixin
from django.contrib import admin
from django.utils.html import format_html
from django import forms
from django.contrib.contenttypes.models import ContentType

from .models import (
    Customer,
    Product,
    ProductImage,
    ProductPrice,
    Transaction,
    Store,
    Order,
)


class ProductPriceInline(SortableAdminMixin, admin.TabularInline):
    model = ProductPrice
    extra = 1


class ProductImageInline(SortableAdminMixin, admin.TabularInline):
    model = ProductImage
    extra = 1

    def image_tag(self, obj):
        return format_html('<img src="{}" width="150" height="auto" />', obj.image.url)

    image_tag.short_description = "Image"

    # Включаем метод в список отображаемых полей
    readonly_fields = [
        "image_tag",
    ]
    fields = ("image", "image_tag", "order")


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline, ProductPriceInline]
    list_display = ("title", "latest_selling_price")

    def latest_selling_price(self, obj):
        return obj.latest_selling_price()

    latest_selling_price.short_description = "Latest Selling Price"



class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["content_type"].queryset = ContentType.objects.filter(
            model__in=["order", "store"]
        )


class TransactionAdmin(admin.ModelAdmin):
    form = TransactionForm

admin.site.register(Product, ProductAdmin)

admin.site.register(ProductPrice)

admin.site.register(Transaction, TransactionAdmin)

admin.site.register(Store)

admin.site.register(Order)

admin.site.register(Customer)
