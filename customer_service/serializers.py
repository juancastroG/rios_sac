from rest_framework import serializers
from .models import Customer, Purchase, PurchaseItem

class CustomerSerializer(serializers.ModelSerializer):
    document_type_name = serializers.CharField(source='document_type.name', read_only=True)
    
    class Meta:
        model = Customer
        fields = ['id', 'document_type_name', 'document_number', 'first_name', 
                 'last_name', 'email', 'phone', 'address']

class PurchaseItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    
    class Meta:
        model = PurchaseItem
        fields = ['product_name', 'quantity', 'unit_price', 'subtotal']

class PurchaseSerializer(serializers.ModelSerializer):
    items = PurchaseItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Purchase
        fields = ['id', 'purchase_date', 'total_amount', 'items']