from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VendorViewSet, PurchaseOrderViewSet, HistoricalPerformanceViewSet, home

router = DefaultRouter()
router.register(r'vendors', VendorViewSet, basename='vendor')
router.register(r'purchase_orders', PurchaseOrderViewSet,
                basename='purchase_order')
router.register(r'historical_performance',
                HistoricalPerformanceViewSet, basename='historical_performance')

urlpatterns = [
    path('', home, name='home'),
    path('api/', include(router.urls)),
]
