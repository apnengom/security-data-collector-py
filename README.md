### Arquitectura del Sistema
Explica por qué elegiste separar las interfaces del controlador.

"Se implementó un Patrón Mediador para centralizar la navegación y el manejo de estados, garantizando que las interfaces (Frames) sean independientes y no arrastren dependencias del motor principal."

### Stack Tecnológico
Lenguaje: Python 3.12+

GUI: CustomTkinter (Optimizado para bajo consumo de recursos en entornos móviles/escritorio).

Backend: Flask (REST API).

Análisis de Datos: PySpark (Procesamiento de logs a gran escala).

Base de Datos: SQLite con integridad referencial (Foreign Keys habilitadas).

### Características de Seguridad (Blue Team Focus)
Detección de Payloads: Analizador de firmas para mitigar SQLi y XSS en el punto de entrada.

Resiliencia de Memoria: Gestión de ciclo de vida de objetos mediante limpieza selectiva de procesos after de Tkinter para evitar fugas de memoria.

Huella Digital: Generación de hashes únicos por cliente para trazabilidad de intentos de acceso.
