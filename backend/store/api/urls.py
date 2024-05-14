from rest_framework.routers import DefaultRouter

from .views import (
    CustomerViewSet,
    ProductViewSet,
    ProductImageViewSet,
    ProductPriceViewSet,
    TransactionViewSet,
    OrderViewSet,
    StoreViewSet,
)

router = DefaultRouter()
router.register(r"customer", CustomerViewSet, basename="customer")

router.register(r"product", ProductViewSet, basename="product")
router.register(
    r"product/(?P<product_id>\d+)/images", ProductImageViewSet, basename="product-image"
)
router.register(
    r"product/(?P<product_id>\d+)/prices", ProductPriceViewSet, basename="product-price"
)

router.register(r"transaction", TransactionViewSet, basename="transaction")

router.register(r"order", OrderViewSet, basename="order")

router.register(r"store", StoreViewSet, basename="store")

urlpatterns = router.urls
