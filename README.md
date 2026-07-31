# 🧠 Quiz App — Sistema de Cuestionarios Dinámicos

¡Bienvenido al repositorio de **Quiz App**! Esta es una aplicación web full-stack robusta, interactiva y de enfoque educativo diseñada para servir como una herramienta pedagógica en el aula. A través de este proyecto, los estudiantes pueden asimilar conceptos fundamentales del desarrollo de software moderno: la arquitectura cliente-servidor, la gestión y diseño de bases de datos relacionales con SQL/SQLite, y el renderizado dinámico en el servidor mediante el sistema de plantillas Jinja2 con Flask.

---

## 🚀 Arquitectura y Características Principales

El proyecto implementa una arquitectura modular bien definida para separar las responsabilidades del frontend, el backend y la persistencia de datos:

### 🌐 Backend y Servidor Web (`app.py`)
* **Controlador Central:** Gestiona el ciclo de vida de las peticiones HTTP (`GET` y `POST`).
* **Enrutamiento Dinámico:** Define las rutas principales de la aplicación web:
  * `/`: Pantalla de bienvenida e inicio del cuestionario.
  * `/test`: Renderizado dinámico de preguntas y captura de respuestas en tiempo real.
  * `/results`: Procesamiento y visualización del puntaje final obtenido por el usuario.
* **Inyección de Contexto:** Extrae la información desde la capa de persistencia y la expone de manera segura al motor de plantillas.

### 💾 Persistencia y Base de Datos SQL (`database.py`)
* **Motor Integrado:** Utiliza SQLite, eliminando la necesidad de configurar servidores de base de datos complejos y permitiendo un almacenamiento local ligero en un único archivo.
* **Modelo de Datos Eficiente:** Tablas estructuradas de forma relacional para almacenar de manera independiente las preguntas, las opciones de respuesta y las claves de corrección.
* **Consultas SQL Puras:** Diseñado didácticamente con sentencias SQL nativas (`CREATE TABLE`, `INSERT INTO`, `SELECT`) para que los alumnos dominen la sintaxis estándar del lenguaje.

### 🎨 Frontend Basado en Plantillas (`templates/` & `static/`)
* **Herencia de Plantillas (Jinja2):** Se utiliza `base.html` como la plantilla maestra que define la estructura global (HTML5, metadatos, barra de navegación y pie de página). Las vistas secundarias heredan este esqueleto mediante bloques de contenido dinámico:
  * `test.html`: Estructura adaptativa para desplegar secuencialmente el banco de preguntas.
  * `results.html`: Tarjeta de puntuación final con retroalimentación inmediata.
* **Aislamiento de Estilos y Comportamiento:** Los estilos responsivos se unifican en `static/css/style.css`.

---

## 📂 Estructura del Proyecto

La disposición de los archivos sigue estrictamente las convenciones de diseño de aplicaciones Flask:

```plaintext
quiz-app/
│
├── templates/               # Capa de Vistas: Plantillas HTML dinámicas (Jinja2)
│   ├── base.html            # Layout maestro (Esqueleto base de la interfaz)
│   ├── test.html            # Contenedor dinámico del cuestionario
│   └── results.html         # Pantalla modular de resultados y feedback
│
├── static/                  # Capa de Recursos Estáticos
│   ├── css/
│   │   └── style.css        # Hoja de estilos general y componentes responsivos
│
├── app.py                   # Capa de Control: Servidor Flask y lógica de negocio
├── database.py              # Capa de Modelo: Inicialización, semillas y consultas SQL
│
└── README.md                # Documentación oficial del proyecto
``` 
