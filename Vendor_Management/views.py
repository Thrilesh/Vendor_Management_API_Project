# views.py

from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from datetime import timezone
from django.db.models import Avg, F
from .models import Vendor, PurchaseOrder, HistoricalPerformance
from .serializers import VendorSerializer, PurchaseOrderSerializer, HistoricalPerformanceSerializer


def home(request):
    return render(request, 'Vendor_Management/home.html')


class VendorViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

    @action(detail=True, methods=['get'])
    def performance(self, request, pk=None):
        vendor = self.get_object()

        # Calculate and return performance metrics
        total_completed_orders = PurchaseOrder.objects.filter(
            vendor=vendor, status='completed'
        ).count()

        on_time_delivery_count = PurchaseOrder.objects.filter(
            vendor=vendor, status='completed', delivery_date__lte=F('acknowledgment_date')
        ).count()
        on_time_delivery_rate = (
            on_time_delivery_count / total_completed_orders) * 100 if total_completed_orders > 0 else 0

        quality_rating_avg = PurchaseOrder.objects.filter(
            vendor=vendor, status='completed', quality_rating__isnull=False
        ).aggregate(Avg('quality_rating'))['quality_rating__avg'] or 0

        average_response_time = PurchaseOrder.objects.filter(
            vendor=vendor, status='completed', acknowledgment_date__isnull=False
        ).aggregate(
            average_response_time=Avg(
                F('acknowledgment_date') - F('issue_date'))
        )['average_response_time'] or 0

        fulfilled_orders = PurchaseOrder.objects.filter(
            vendor=vendor, status='completed', issue_date__isnull=True
        ).count()

        fulfillment_rate = (fulfilled_orders / total_completed_orders) * \
            100 if total_completed_orders > 0 else 0

        performance_data = {
            'on_time_delivery_rate': on_time_delivery_rate,
            'quality_rating_avg': quality_rating_avg,
            'average_response_time': average_response_time,
            'fulfillment_rate':  fulfillment_rate,
        }

        return Response(performance_data)

    @action(detail=False, methods=['post'])
    def acknowledge_order(self, request):
        # Assuming the request includes the purchase order ID
        po_id = request.data.get('po_id')
        try:
            purchase_order = PurchaseOrder.objects.get(id=po_id)
            purchase_order.acknowledgment_date = timezone.now()
            purchase_order.save()

            # Trigger recalculation of average_response_time
            purchase_order.vendor.calculate_average_response_time()

            return Response({'message': 'Acknowledgment successful'})
        except PurchaseOrder.DoesNotExist:
            return Response({'error': 'Purchase Order does not exist'}, status=status.HTTP_404_NOT_FOUND)


class PurchaseOrderViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer


class HistoricalPerformanceViewSet(viewsets.ModelViewSet):
    queryset = HistoricalPerformance.objects.all()
    serializer_class = HistoricalPerformanceSerializer
