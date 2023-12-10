from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from .models import Vendor, PurchaseOrder


class VendorManagementTests(TestCase):
    def setUp(self):
        # Set up test data or create instances needed for testing
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')
        self.client = APIClient()

        # Create a sample vendor for testing
        self.vendor = Vendor.objects.create(
            name='Test Vendor',
            contact_details='test@example.com',
            address='123 Test Street',
            vendor_code='VENDOR001',
        )

        # Create a sample purchase order for testing
        self.purchase_order = PurchaseOrder.objects.create(
            po_number='PO001',
            vendor=self.vendor,
            order_date='2023-01-01',
            delivery_date='2023-01-10',
            items={'item1': 10, 'item2': 20},
            quantity=30,
            status='pending',
            quality_rating=4.5,
            issue_date='2023-01-02',
        )

    def test_vendor_list_endpoint(self):
        # Test the vendor list API endpoint
        response = self.client.get('/api/vendors/')
        self.assertEqual(response.status_code, 200)

    def test_vendor_detail_endpoint(self):
        # Test the vendor detail API endpoint
        response = self.client.get(f'/api/vendors/{self.vendor.id}/')
        self.assertEqual(response.status_code, 200)

    def test_purchase_order_list_endpoint(self):
        # Test the purchase order list API endpoint
        response = self.client.get('/api/purchase_orders/')
        self.assertEqual(response.status_code, 200)

    def test_purchase_order_detail_endpoint(self):
        # Test the purchase order detail API endpoint
        response = self.client.get(
            f'/api/purchase_orders/{self.purchase_order.id}/')
        self.assertEqual(response.status_code, 200)

    def test_vendor_performance_endpoint(self):
        # Test the vendor performance API endpoint
        response = self.client.get(
            f'/api/vendors/{self.vendor.id}/performance/')
        self.assertEqual(response.status_code, 200)


def test_acknowledge_purchase_order_endpoint(self):
    # Test the acknowledge purchase order API endpoint
    response = self.client.post(
        f'/api/purchase_orders/{self.purchase_order.id}/acknowledge/')
    print(response.content)
    self.assertEqual(response.status_code, 200)

    def test_data_integrity(self):
        # Test scenarios to ensure data integrity
        # For example, check if calculations handle division by zero or missing data gracefully
        pass
