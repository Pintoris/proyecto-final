Markdown# 🎮 Laberintos Extremos — Arcade Retro & Motor de Videojuegos 2D

¡Bienvenido al repositorio de **Laberintos Extremos**! Esta es una aplicación de videojuegos 2D desarrollada en Python con la librería Pygame. El proyecto está diseñado como una herramienta pedagógica para que los estudiantes comprendan los cimientos de la programación de videojuegos: el bucle principal (Game Loop), la gestión de estados, la física de colisiones rectangulares (AABB), el renderizado de gráficos vectoriales/sprites y sistemas de partículas.

---

## 🚀 Arquitectura y Características Principales

El proyecto implementa una arquitectura basada en un bucle de eventos centrado en un máquina de estados finitos (FSM) para gestionar la transición entre menús y partidas, optimizado a 60 FPS estables.

```plaintext
                   +------------------------+
                   |     MENÚ PRINCIPAL     |
                   +-----------+------------+
                               |
                               v
                   +------------------------+
                   |   SELECCIÓN DE MAPA    |
                   +-----------+------------+
                               |
                               v
                   +------------------------+
                   |   PANTALLA DE JUEGO    |
                   +-----+------------+-----+
                         |            |
            (Colisión)   |            |   (Llega a la meta)
                         v            v
                   +-----------+  +-----------+
                   | DERROTADO |  | VICTORIA  |
                   +-----------+  +-----------+
🧠 Bucle Principal y Gestión de Estados (main.py / laberinto.py)Controlador de Estados: Mantiene la fluidez entre menu_principal, seleccion_mapa, jugando, derrotado y victoria.Sincronización Táctil (Clock): Uso de clock.tick(60) para garantizar un renderizado fluido e independiente de la potencia de procesamiento del CPU.👾 Objetos Dinámicos y Física (M_c, Pared, Particula)POO en Videojuegos: Implementación de herencia mediante pygame.sprite.Sprite.Motor de Colisiones: Uso de cajas envolventes AABB (Axis-Aligned Bounding Box) con sprite.collide_rect y Rect.collidepoint.I.A. Enemiga Lineal: Patrullaje de enemigos en ejes X/Y con rebote automático al alcanzar los límites del mapa (limite_min, limite_max).Efectos Visuales (Partículas & FX): Generador de partículas con desvanecimiento de canal alfa (SRCALPHA) que reaccionan al movimiento del jugador y de los enemigos.🎨 Renderizado y Componentes de Interfaz (UI)Pintado Dinámico de Grid: Creación de un fondo procedural estilo Cyberpunk/Modern Arcade.Efectos de Glow y Animación Matemática: Animación de pulsación en la celda de la Meta mediante funciones trigonométricas (math.sin(tiempo)).Botones Interactivos UI: Manejo de estados de ratón (Hover y Click) dibujando sombras y bordes dinámicos.📂 Estructura del ProyectoLa disposición de los archivos mantiene una estructura limpia, ligera y autocontenida:Plaintextlaberintos-extremos/
│
├── hero.png                 # Sprite/Imagen del personaje jugable
├── cyborg.png               # Sprite/Imagen de los enemigos
│
├── juego.py                 # Código fuente principal (Game Loop, Clases y Mapas)
├── requirements.txt         # Lista de dependencias (Pygame)
├── .gitignore               # Exclusión de archivos no deseados en Git
└── README.md                # Documentación oficial del proyecto
🛠️ Tecnologías UtilizadasComponenteTecnologíaDescripciónLenguajePython 3.xLenguaje base orientado a objetos.Motor 2DPygameLibrería multimedia para renderizado 2D, eventos de teclado y audio.MatemáticaStandard Library (math, random)Funciones trigonométricas para animaciones e I.A. con aleatoriedad.GráficosSurface / PNGRenderizado vectorial directo en GPU/CPU con soporte de transparencias.🚀 Guía de Configuración y DespliegueSigue estos pasos detallados para preparar tu entorno de desarrollo y ejecutar el juego en cualquier equipo.Paso 1: Crear el archivo de dependencias (requirements.txt)Para registrar la librería Pygame necesaria para ejecutar el proyecto, ejecuta en tu terminal:Bashpip freeze > requirements.txt
Paso 2: Configurar la exclusión de Git (.gitignore)Para evitar subir el entorno virtual y archivos temporales de Python a GitHub:Bashecho "venv/" > .gitignore
echo "__pycache__/" >> .gitignore
🛠️ Cómo Replicar este Proyecto en otra ComputadoraSi clonas o descargas este proyecto en una computadora nueva, sigue estos comandos en la terminal:1. Crear un entorno virtualBashpython3 -m venv venv
2. Activar el entorno virtualEn Linux/macOS:Bashsource venv/bin/activate
En Windows (PowerShell):PowerShell.\venv\Scripts\Activate.ps1
3. Instalar las dependenciasBashpip install -r requirements.txt
4. Ejecutar el juegoBashpython juego.py
🔄 Flujo de Trabajo DiarioAbrir la terminal en la carpeta raíz del proyecto.Activar el entorno: source venv/bin/activate (Verás el indicador (venv) al inicio).Ejecutar el videojuego: python juego.py.Salir del entorno (opcional): Escribe deactivate.📝 Guía Metodológica y Ejercicios para ClaseEste proyecto está diseñado para guiar laboratorios prácticos de lógica de programación orientada a objetos y videojuegos:💡 Laboratorio 1: Diseño Procedural y Creación de Niveles (cargar_mapa)Desafío: Pide a los estudiantes que añadan un Mapa 4. Deben instanciar nuevas estructuras de Pared y enemigos con diferentes rutas de patrullaje para entender las coordenadas $X, Y$ en un plano cartesiano donde $(0,0)$ es la esquina superior izquierda.💡 Laboratorio 2: Modificación de Sprites y AssetsDesafío: Modificar la carga de imágenes (PLAYER1_IMAG y PLAYER2_IMAG). Los alumnos aprenderán sobre el reescalado de imágenes con transform.scale() y la importancia de controlar las dimensiones (Rect) para evitar errores de colisión visualmente invisibles.💡 Laboratorio 3: Física y Mecánicas (Aumento de Dificultad)Desafío: Implementar un acelerador o potenciador (Power-up). Los alumnos deben crear una nueva clase Item que, al colisionar con el jugador, incremente la propiedad self.speed del personaje por un tiempo limitado.
