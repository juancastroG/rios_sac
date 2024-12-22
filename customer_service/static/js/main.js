document.addEventListener('DOMContentLoaded', function() {
    const searchForm = document.getElementById('searchForm');
    const resultsDiv = document.getElementById('results');

    // Evento de click en el boton enviar
    searchForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const documentNumber = document.getElementById('documentNumber').value;
        const loadingDiv = showLoading();
    
        try {
            const response = await fetch(`/api/customer/${documentNumber}/`);
            const data = await response.json();
    
            if (!response.ok) {
                throw new Error(data.error || 'Error al buscar cliente');
            }
    
            if (!data.customers || data.customers.length === 0) {
                throw new Error('No se encontraron clientes');
            }
    
            displayCustomerData(data);
            
            resultsDiv.classList.remove('hidden');
    
        } catch (error) {
            showError(error.message);
        } finally {
            loadingDiv.remove();
        }
    });
    // Función para mostrar loading
    function showLoading() {
        const loading = document.createElement('div');
        loading.className = 'fixed top-0 left-0 w-full h-full flex items-center justify-center bg-black bg-opacity-50';
        loading.innerHTML = `
            <div class="bg-white p-4 rounded-lg shadow-lg">
                <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
                <p class="mt-2">Buscando...</p>
            </div>
        `;
        document.body.appendChild(loading);
        return loading;
    }

    // Función para mostrar datos del cliente
    function displayCustomerData(data) {
        const { customers, purchases_by_customer } = data;
        
        resultsDiv.innerHTML = `
            <div class="space-y-6">
                <h2 class="text-2xl font-bold mb-4">Resultados de la búsqueda</h2>
                ${customers.map(customer => `
                    <div class="border rounded-lg p-6 mb-6 shadow-sm">
                        <div class="border-b pb-4">
                            <h3 class="text-xl font-bold mb-4">Información del Cliente</h3>
                            <div class="grid grid-cols-2 gap-4">
                                <div>
                                    <p class="text-gray-600">Documento</p>
                                    <p class="font-medium">${customer.document_type_name} ${customer.document_number}</p>
                                </div>
                                <div>
                                    <p class="text-gray-600">Nombre</p>
                                    <p class="font-medium">${customer.first_name} ${customer.last_name}</p>
                                </div>
                                <div>
                                    <p class="text-gray-600">Email</p>
                                    <p class="font-medium">${customer.email}</p>
                                </div>
                                <div>
                                    <p class="text-gray-600">Teléfono</p>
                                    <p class="font-medium">${customer.phone}</p>
                                </div>
                            </div>
                        </div>
    
                        <div class="mt-4">
                            <h3 class="text-lg font-bold mb-4">Compras Recientes</h3>
                            <div class="overflow-x-auto">
                                <table class="min-w-full divide-y divide-gray-200">
                                    <thead>
                                        <tr>
                                            <th class="px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Fecha</th>
                                            <th class="px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Total</th>
                                            <th class="px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Productos</th>
                                        </tr>
                                    </thead>
                                    <tbody class="bg-white divide-y divide-gray-200">
                                        ${(purchases_by_customer[customer.id] || []).map(purchase => `
                                            <tr>
                                                <td class="px-6 py-4 whitespace-nowrap">
                                                    ${new Date(purchase.purchase_date).toLocaleDateString()}
                                                </td>
                                                <td class="px-6 py-4 whitespace-nowrap">
                                                    $${purchase.total_amount.toLocaleString()}
                                                </td>
                                                <td class="px-6 py-4">
                                                    <ul class="list-disc list-inside">
                                                        ${purchase.items.map(item => `
                                                            <li>${item.product_name} (${item.quantity})</li>
                                                        `).join('')}
                                                    </ul>
                                                </td>
                                            </tr>
                                        `).join('')}
                                    </tbody>
                                </table>
                            </div>
                        </div>
    
                        <div class="flex justify-end space-x-4 mt-6">
                            <button onclick="exportCustomerData('${customer.document_number}')"
                                    class="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600 transition-colors">
                                Exportar Datos
                            </button>
                        </div>
                    </div>
                `).join('')}
                
                ${customers.length === 0 ? `
                    <div class="text-center py-8 text-gray-500">
                        No se encontraron resultados
                    </div>
                ` : ''}
            </div>
        `;
    }

    // Función para mostrar errores
    function showError(message) {
        resultsDiv.innerHTML = `
            <div class="bg-red-50 border-l-4 border-red-500 p-4">
                <div class="flex">
                    <div class="flex-shrink-0">
                        <svg class="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"/>
                        </svg>
                    </div>
                    <div class="ml-3">
                        <p class="text-sm text-red-700">${message}</p>
                    </div>
                </div>
            </div>
        `;
        resultsDiv.classList.remove('hidden');
    }
});

// Función para exportar datos
async function exportCustomerData(documentNumber) {
    try {
        const response = await fetch(`/api/export-customer/${documentNumber}/`);
        if (!response.ok) throw new Error('Error al exportar datos');

        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `cliente_${documentNumber}.xlsx`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        a.remove();
    } catch (error) {
        console.error('Error:', error);
        alert('Error al exportar los datos');
    }
}

// Función para descargar reporte de fidelidad (mayor a 5000000 en compras) 
async function downloadLoyaltyReport() {
    try {
        const response = await fetch('/api/loyalty-report/');
        
        if (!response.ok) {
            if (response.status === 404) {
                alert('No se encontraron clientes que cumplan los criterios de fidelización');
                return;
            }
            throw new Error('Error al generar el reporte');
        }

        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        const date = new Date().toISOString().slice(0, 7);
        
        a.href = url;
        a.download = `reporte_fidelizacion_${date}.xlsx`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        a.remove();
        
    } catch (error) {
        console.error('Error:', error);
        alert('Error al descargar el reporte de fidelización');
    }
}
