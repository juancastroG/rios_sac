from django.db import models
from django.core.validators import EmailValidator, MinValueValidator
from django.utils import timezone

class DocumentType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

class Customer(models.Model):
    document_type = models.ForeignKey(DocumentType, on_delete=models.PROTECT)
    document_number = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(validators=[EmailValidator()])
    phone = models.CharField(max_length=15)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        indexes = [
            models.Index(fields=['document_number']),
        ]
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class ProductCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(ProductCategory, on_delete=models.PROTECT)
    description = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

class Purchase(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='purchases')
    purchase_date = models.DateTimeField(default=timezone.now)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    notes = models.TextField(null=True, blank=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['purchase_date', 'customer']),
        ]

class PurchaseItem(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.PROTECT, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)