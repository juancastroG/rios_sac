# admin.py
from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect
from django.contrib import messages
from customer_service.views import generate_loyalty_report


from .models import (
    DocumentType, Customer, ProductCategory, 
    Product, Purchase, PurchaseItem
)

@admin.register(DocumentType)
class DocumentTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    search_fields = ('name', 'code')

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('document_number', 'first_name', 'last_name', 'email', 'phone')
    search_fields = ('document_number', 'first_name', 'last_name', 'email')
    list_filter = ('document_type', 'is_active')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                'loyalty-report/',
                self.admin_site.admin_view(self.generate_loyalty_report_view),
                name='loyalty-report'
            ),
        ]
        return custom_urls + urls

    def generate_loyalty_report_view(self, request):
        try:
            return generate_loyalty_report(request)
        except Exception as e:
            messages.error(request, f'Error generando reporte: {str(e)}')
            return redirect('..')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'is_active')
    search_fields = ('name',)
    list_filter = ('category', 'is_active')

class PurchaseItemInline(admin.TabularInline):
    model = PurchaseItem
    extra = 1

@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'purchase_date', 'total_amount')
    search_fields = ('customer__document_number', 'customer__first_name')
    list_filter = ('purchase_date',)
    inlines = [PurchaseItemInline]