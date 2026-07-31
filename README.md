# 🎮 Laberintos Extremos — Arcade Retro & Motor de Videojuegos 2D

¡Bienvenido al repositorio de **Laberintos Extremos**! Esta es una aplicación de videojuegos 2D desarrollada en Python con la librería Pygame. El proyecto está diseñado como una **herramienta pedagógica** para que los estudiantes comprendan los cimientos de la programación de videojuegos: el bucle principal (*Game Loop*), la gestión de estados, la física de colisiones rectangulares (AABB), el renderizado de gráficos vectoriales/sprites y sistemas de partículas.

---

## 🚀 Arquitectura y Características Principales

El proyecto implementa una arquitectura basada en un bucle de eventos centrado en una **máquina de estados finitos (FSM)** para gestionar la transición entre menús y partidas, optimizado a 60 FPS estables.

`
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
                   

Componente,Tecnología
Backend,Python 3.x
BD,SQLite3
