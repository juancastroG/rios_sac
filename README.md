# Sistema de Gestión de Clientes - Rios del desierto SAS 🏢

## Descripción 📋
Sistema web desarrollado en Django para el equipo de Servicio al Cliente (SAC) que permite consultar información detallada de clientes mediante su número de documento, optimizar tiempos de atención y gestionar programas de fidelización.

## Características Principales ⭐
- Consulta rápida de clientes por número de documento
- Exportación de datos a Excel
- Generación de reportes de fidelización
- Interfaz web intuitiva y responsive
- API RESTful para integración con otros sistemas

## Tecnologías Utilizadas 🛠️
- **Backend**: Django, Django REST Framework
- **Frontend**: HTML5, JavaScript, Tailwind CSS
- **Base de Datos**: SQLite
- **Librerías**: Pandas, openpyxl
- **Otras herramientas**: Git, CloudPanel (Despliegue)

## Estructura del Proyecto 📁
```
proyecto/
├── customer_service/         # Aplicación principal
│   ├── migrations/          # Migraciones de la base de datos
│   ├── static/             # Archivos estáticos
│   ├── templates/          # Plantillas HTML
│   ├── models.py           # Modelos de la base de datos
│   ├── views.py            # Vistas y lógica de negocio
│   ├── urls.py            # Configuración de URLs
│   └── serializers.py      # Serializadores para la API
├── rios_sac/               # Configuración del proyecto
│   ├── settings.py        # Configuraciones generales
│   ├── urls.py           # URLs principales
│   └── wsgi.py           # Configuración WSGI
└── requirements.txt        # Dependencias del proyecto
```

## Modelos de Datos 💾
- **DocumentType**: Tipos de documento (NIT, Cédula, Pasaporte)
- **Customer**: Información básica del cliente
- **ProductCategory**: Categorías de productos
- **Product**: Catálogo de productos
- **Purchase**: Registro de compras
- **PurchaseItem**: Detalle de productos por compra

## Funcionalidades Principales 🔍
1. **Búsqueda de Clientes**
   - Búsqueda por número de documento
   - Visualización de datos personales
   - Historial de compras recientes

2. **Exportación de Datos**
   - Exportación a Excel de información del cliente
   - Historial detallado de compras

3. **Reportes de Fidelización**
   - Generación de reportes mensuales
   - Filtrado de clientes con compras superiores a $5,000,000 COP
   - Análisis de patrones de compra

## Guía de Instalación 🚀

### Requisitos Previos
- Python 3.11 o superior
- pip (gestor de paquetes de Python)
- Acceso SSH al servidor (para despliegue)

### Instalación Local
1. Clonar el repositorio
   ```bash
   git clone [URL_DEL_REPOSITORIO]
   cd [NOMBRE_DEL_PROYECTO]
   ```

2. Crear y activar entorno virtual
   ```bash
   python -m venv env
   source env/bin/activate  # En Windows: env\Scripts\activate
   ```

3. Instalar dependencias
   ```bash
   pip install -r requirements.txt
   ```

4. Configurar la base de datos
   ```bash
   python manage.py migrate
   ```

5. Crear superusuario (opcional)
   ```bash
   python manage.py createsuperuser
   ```

6. Iniciar servidor de desarrollo
   ```bash
   python manage.py runserver
   ```

### Despliegue en Producción
Consultar el archivo `Guía de Despliegue de Django en CloudPanel.pdf` para instrucciones detalladas sobre el despliegue en CloudPanel.

## API Endpoints 🔗
- `GET /api/customer/<document_number>/`: Obtiene detalles del cliente
- `GET /api/export-customer/<document_number>/`: Exporta datos del cliente a Excel
- `GET /api/loyalty-report/`: Genera reporte de fidelización

## Autor ✒️
- Juan Carlos Castro Guevara
- Contacto: [juankstro77@hotmail.com]
