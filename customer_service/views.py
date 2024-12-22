from io import BytesIO
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from rest_framework import generics
from rest_framework.response import Response
from datetime import datetime, timedelta
import pandas as pd
from .models import Customer, Purchase, PurchaseItem
from .serializers import CustomerSerializer, PurchaseSerializer
from django.db.models import Sum

def search_view(request):
    """Vista principal para el formulario de búsqueda"""
    return render(request, 'customer_service/search.html')

# Api para obtener los detalles de los clientes desde la BD
class CustomerDetailAPI(generics.RetrieveAPIView):
    """API para obtener detalles del cliente y sus compras"""
    serializer_class = CustomerSerializer
    lookup_field = 'document_number'

    def get_queryset(self):
        document_number = self.kwargs.get('document_number', '')
        query_Set = Customer.objects.filter(document_number__startswith = document_number)
        return query_Set

    def retrieve(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        
        if not queryset.exists():
            return Response(
                {'error': 'No se encontraron clientes'}, 
                status=404
            )
            
        customers_data = CustomerSerializer(queryset, many=True).data
        
        purchases_by_customer = {}
        for customer in queryset:
            recent_purchases = Purchase.objects.filter(
                customer=customer
            ).order_by('-purchase_date')[:5]
            
            purchases_by_customer[customer.id] = PurchaseSerializer(
                recent_purchases, 
                many=True
            ).data
        
        return Response({
            'customers': customers_data,
            'purchases_by_customer': purchases_by_customer
        })

# Función para exportar datos del cliente a un excel
def export_customer_data(request, document_number):
    """Exporta los datos del cliente a Excel"""
    try:
        customer = Customer.objects.get(document_number=document_number)
        purchases = Purchase.objects.filter(customer=customer)

        # Crear DataFrame con datos del cliente
        customer_data = {
            'Tipo Documento': [customer.document_type.name],
            'Número Documento': [customer.document_number],
            'Nombre': [customer.first_name],
            'Apellido': [customer.last_name],
            'Email': [customer.email],
            'Teléfono': [customer.phone]
        }
        df_customer = pd.DataFrame(customer_data)

        # Crear DataFrame con compras
        purchase_data = []
        for purchase in purchases:
            for item in purchase.items.all():
                purchase_data.append({
                    'Fecha': purchase.purchase_date,
                    'Producto': item.product.name,
                    'Cantidad': item.quantity,
                    'Precio Unitario': item.unit_price,
                    'Subtotal': item.subtotal
                })
        df_purchases = pd.DataFrame(purchase_data)
        df_purchases['Fecha'] = df_purchases['Fecha'].dt.tz_localize(None)

        # Crear Excel con múltiples hojas
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df_customer.to_excel(writer, sheet_name='Datos Cliente', index=False)
            df_purchases.to_excel(writer, sheet_name='Historial Compras', index=False)

        output.seek(0)
        response = HttpResponse(
            output.read(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename=cliente_{document_number}.xlsx'
        return response

    except Customer.DoesNotExist:
        return JsonResponse({'error': 'Cliente no encontrado'}, status=404)

# Función para descargar los datos del reporte de fidelidad (Usuarios que gastan mas de 5 millones en el ultimo mes)
def generate_loyalty_report(request):
    """
    Genera reporte de clientes potenciales para fidelización basado en:
    - Compras del mes anterior
    - Monto total superior a 5 millones COP
    """
    # Obtener el rango del mes anterior
    today = timezone.now()
    first_day = (today.replace(day=1) - timedelta(days=1)).replace(day=1)
    last_day = today.replace(day=1) - timedelta(days=1)
    potential_customers = (
        Customer.objects
        .filter(
            purchases__purchase_date__range=(first_day, last_day)
        )
        .annotate(
            total_month=Sum('purchases__total_amount', default=0)
        )
        .filter(total_month__gte=5000000)
        .prefetch_related('purchases')
    )

    report_data = []
    for customer in potential_customers:
        report_data.append({
            'Tipo de Documento': customer.document_type.name,
            'Número de Documento': customer.document_number,
            'Nombre Completo': f"{customer.first_name} {customer.last_name}",
            'Email': customer.email,
            'Teléfono': customer.phone,
            'Total Compras Último Mes': customer.total_month,
            'Número Total de Compras': customer.purchases.count(),
            'Cliente Desde': customer.created_at.strftime('%Y-%m-%d'),
        })
    if not report_data:
        return JsonResponse({
            'message': 'No se encontraron clientes que cumplan los criterios de fidelización'
        }, status=404)

    df = pd.DataFrame(report_data)
    
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Clientes Fidelización')
        
        worksheet = writer.sheets['Clientes Fidelización']
        
    output.seek(0)
    
    filename = f'clientes_fidelizacion_{first_day.strftime("%Y-%m")}.xlsx'
    
    response = HttpResponse(
        output.read(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename={filename}'
    
    return response