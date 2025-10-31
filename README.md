<<<<<<< HEAD
# **ViviendaYa – Marketplace Inmobiliario**

## **Universidad Autónoma de Ciudad Juárez**

**Campus CU-IIT**
**Materia:** 20250812 IEC-9844-00 A – *Innovación Tecnológica*
**Profesor:** Dr. Abraham López Nájera
**Equipo:** 5


## **Integrantes del Equipo**

| **Nombre**                      | **Matrícula** |
| ------------------------------- | ------------- |
| Andrés Yahir Almanza Quezada    | 215993        |
| Neida Cristina Franco Escobedo  | 214981        |
| Brandon Gustavo Hernández Ortiz | 192880        |
| David Cano Muñiz                | 215814        |
| Leonardo Ortega Escobar         | 215579        |


## **Descripción General del Proyecto**

ViviendaYa es un marketplace inmobiliario desarrollado con el framework Django, orientado a centralizar la oferta de propiedades en la ciudad de Ciudad Juárez, Chihuahua.
El proyecto tiene como propósito facilitar el proceso de compra, venta y renta de inmuebles residenciales y comerciales, brindando una alternativa tecnológica segura, eficiente y accesible para todos los usuarios involucrados en el mercado inmobiliario local.

El sistema permite a agentes, constructoras e inmobiliarias publicar sus propiedades, gestionar anuncios y establecer comunicación directa con posibles compradores o arrendatarios. Además, ofrece herramientas de búsqueda avanzada, visualización georreferenciada y verificación de identidad, garantizando un entorno confiable para la interacción entre oferentes y demandantes.

Este desarrollo surge como respuesta a la creciente digitalización del sector inmobiliario y a la necesidad de reducir los fraudes y los procesos informales que actualmente se realizan a través de redes sociales.
La plataforma se distingue por su escalabilidad, su interfaz intuitiva y su integración con servicios modernos como autenticación segura (Django Allauth) y pagos en línea (Stripe).


## **Objetivo General**

Diseñar e implementar un sistema web funcional y escalable que permita la gestión integral de propiedades inmobiliarias, optimizando los procesos de publicación, búsqueda, comunicación y control de usuarios, bajo un entorno ágil de desarrollo.

## **Características Principales**

* Sistema de registro y autenticación de usuarios mediante Django Allauth.
* Gestión de publicaciones (creación, edición, eliminación y visualización).
* Filtros de búsqueda avanzados: ubicación, tipo de propiedad, rango de precios y características específicas.
* Visualización de inmuebles en mapas interactivos.
* Integración con Stripe para pagos seguros en línea.
* Contacto directo entre cliente y anunciante mediante correo electrónico o WhatsApp.
* Interfaz adaptable y moderna desarrollada con HTML, CSS y Bootstrap.
* Organización modular conforme a los principios de **Scrum**, permitiendo desarrollo incremental.

## **Requisitos de Instalación**

### **1. Requisitos Previos**

Antes de instalar el sistema, asegúrese de contar con los siguientes componentes:

* Python 3.10 o superior
* Django 5.0 o superior
* pip (administrador de paquetes)
* Entorno virtual (*venv*)
* Git (para control de versiones)
* SQLite o PostgreSQL (según configuración del entorno)
* Navegador moderno (Chrome, Edge o Firefox)

**Opcionales:**

* Figma
* Cuenta de Stripe 
* Configuración de correo electrónico 

### **2. Instalación del Proyecto**

Para la instalación y ejecución del entorno local, siga los pasos indicados:

```bash
# 1. Clonar el repositorio
git clone https://github.com/David-P3FES/Innovacion-Tecnologica---Equipo-5.git
cd Innovacion-Tecnologica---Equipo-5

# 2. Crear un entorno virtual
python -m venv venv
source venv/bin/activate   # En Windows: venv\Scripts\activate

# 3. Instalar las dependencias
pip install -r requirements.txt

# 4. Configurar las variables de entorno (.env)
# SECRET_KEY, configuración de base de datos, STRIPE_API_KEY, EMAIL_HOST_USER, etc.

# 5. Realizar migraciones
python manage.py makemigrations
python manage.py migrate

# 6. Crear un superusuario
python manage.py createsuperuser

# 7. Ejecutar el servidor de desarrollo
python manage.py runserver
```

Una vez iniciado el servidor, acceda a la aplicación desde su navegador en la dirección:
**[http://127.0.0.1:8000](http://127.0.0.1:8000)**

## **Estructura del Proyecto**

El proyecto está organizado conforme a una estructura modular propia de Django, en la cual cada aplicación (app) representa un componente funcional del sistema.
Esta organización permite el desarrollo simultáneo por parte de varios integrantes, facilita el mantenimiento del código y favorece la escalabilidad futura del proyecto.

```
INNOVACION-TECNOLOGICA/
│
├── cuentas/                     # Aplicación encargada de la autenticación y gestión de usuarios.
│                                # Incluye registro, inicio de sesión y administración de perfiles.
│
├── diagrams/                    # Diagramas de arquitectura, entidad-relación y documentación técnica.
│
├── docs/                        # Carpeta de documentación general: fases, minutas, reportes y anexos.
│
├── media/                       # Archivos multimedia cargados por los usuarios (fotografías y recursos).
│
├── principal/                   # Aplicación que gestiona las vistas principales del sitio y la navegación.
│
├── publicaciones/               # Aplicación encargada del CRUD de publicaciones inmobiliarias.
│
├── templates/                   # Plantillas HTML reutilizables que definen la interfaz del sistema.
│
├── vivienda/                    # Configuración principal del proyecto Django (settings, urls, wsgi).
│
├── .gitattributes               # Configuración de atributos de archivos para control de versiones.
│
├── .gitignore                   # Archivos y carpetas excluidos del repositorio.
│
├── db.sqlite3                   # Base de datos local para pruebas y entorno de desarrollo.
│
├── Doxyfile                     # Archivo de configuración para la generación de documentación técnica (Doxygen).
│
├── manage.py                    # Script administrativo principal de Django.
│
├── README.md                    # Documento informativo y guía técnica del proyecto.
│
└── requirements.txt             # Dependencias y librerías necesarias para la ejecución del sistema.
```

## **Metodología de Desarrollo**

El desarrollo de ViviendaYa se realizó utilizando la metodología ágil Scrum, la cual permitió la planificación iterativa e incremental de entregables funcionales.
El proceso se organizó mediante sprints semanales, con reuniones de seguimiento, revisión y retrospectiva, documentadas formalmente en minutas y reportes de avance.

Durante el desarrollo se utilizaron las siguientes herramientas:

* **ClickUp:** para la planificación de tareas, definición de Product Backlog y Sprint Backlog.
* **GitHub:** para el control de versiones y la colaboración del equipo.
* **Figma:** para el diseño de la interfaz de usuario y la representación visual del sistema.
* **Django Framework:** como base tecnológica del desarrollo.

Los artefactos generados incluyen:

* Documento de requisitos funcionales y no funcionales (SRS).
* Product Backlog y Sprint Backlog.
* Plan de trabajo y cronograma de actividades.
* Análisis FODA.
* Reportes semanales y minutas de reuniones.


=======
# 🏠 "VIVIENDAYA" - Encontrar el lugar ideal para vivir o invertir
Universidad Autónoma de Ciudad Juárez

---

### 🌵 **Campus CU-IIT**

- **Materia:** 20250812 IEC-9844-00 A INNOVACION TECNOLOGICA
- **Equipo:** 5
- **Profesor:** Abraham Lopez Najera

---

### 🏡 **Nombre del Proyecto: ViviendaYa**

ViviendaYa es una plataforma innovadora que se especializa en la compra, venta y renta de propiedades residenciales y comerciales, ofreciendo atención personalizada y un alto compromiso con la satisfacción del cliente.

---

### 👥 **Integrantes del Equipo**

| **Nombre**          | **Matricula**                 |
|---------------------|-------------------------|
| Andres Almanza       | 215993 |
| Neida Escobedo       | 214981   |
| Brandon Hernandez    | 192880     |
| David Cano           | 215814          |
| Leonardo Ortega      | 215579                   |

---
>>>>>>> Home-Front-clean
