# Guía para Agentes de IA en MetanoIA

## Descripción del Proyecto

MetanoIA es un proyecto educativo de código abierto que busca enseñar una nueva forma de programar con inteligencia artificial. El nombre combina "Meta" (más allá) y "noIA" (inversión de IA), representando un enfoque donde el usuario aprende a través de la co-creación con asistentes de IA, manteniendo siempre el control y la comprensión del proceso.

## Estructura del Repositorio

```
MetanoIA/
├── app.py                 # Punto de entrada principal de la aplicación
├── chat_bot.py            # Implementación principal del chatbot
├── docs/                  # Documentación del proyecto
│   ├── process.md         # Registro cronológico del proceso
│   ├── grimorio-proyecto.md # Compendio de información del proyecto
│   ├── problemas_y_propuestas.md # Problemas detectados y soluciones
│   ├── integracion_*.md   # Documentos de integración de funcionalidades
│   └── reglas_proyecto.md # Reglas y procedimientos del proyecto
├── src/                   # Código fuente
│   ├── api/               # Integraciones con APIs externas
│   ├── components/        # Componentes de la interfaz de usuario
│   ├── models/            # Modelos y lógica de negocio
│   └── utils/             # Utilidades y herramientas auxiliares
├── tareas_diarias/        # Registro y planificación de tareas diarias
└── requirements.txt       # Dependencias del proyecto
```

## Reglas para Agentes de IA

### Filosofía del Proyecto

1. **Aprendizaje sobre automatización**: El objetivo principal es que el usuario comprenda lo que está construyendo, no solo obtener resultados rápidos.
2. **Usuario al mando**: El usuario siempre debe tener la última palabra en las decisiones de diseño e implementación.
3. **Explicación didáctica**: Cada recomendación o solución debe venir acompañada de una explicación clara y educativa.
4. **Español como idioma principal**: Toda la comunicación y documentación debe ser en español claro y accesible.

### Pautas de Contribución

1. **Documentación exhaustiva**: Todo el código debe incluir docstrings completos siguiendo el formato establecido (propósito, parámetros, retornos, excepciones).
2. **Separación de responsabilidades**: Mantener una clara separación entre componentes, APIs y utilidades.
3. **Patrones consistentes**: Seguir los patrones de código establecidos en `reglas_proyecto.md`.
4. **Documentación bajo demanda**: Los archivos de documentación solo deben generarse o actualizarse cuando el usuario lo solicite explícitamente.

### Áreas en Desarrollo Activo

1. **Integración de modelos**: Mejora del sistema para cambiar entre diferentes modelos de lenguaje manteniendo el contexto.
2. **Capacidades de visión**: Integración de modelos multimodales para análisis de imágenes.
3. **Procesamiento de archivos**: Mejora de las capacidades para generar y procesar diferentes tipos de archivos.
4. **Herramientas agénticas**: Desarrollo de herramientas que permiten al asistente realizar acciones específicas.

## Validación de Cambios

Antes de considerar completa cualquier contribución, verificar:

1. **Revisión de código**: ¿El código sigue los patrones establecidos?
2. **Documentación**: ¿Está todo documentado adecuadamente con docstrings?
3. **Pruebas manuales**: ¿La funcionalidad trabaja como se espera?
4. **Integración**: ¿Se integra correctamente con el resto del sistema?
5. **Valor educativo**: ¿El proceso y resultado son comprensibles para el usuario?

## Cómo Trabajar en este Repositorio

### Exploración del Contexto

1. Revisar primero los archivos de documentación en `docs/` para entender la funcionalidad que se está modificando.
2. Consultar `grimorio-proyecto.md` para una visión general del proyecto.
3. Revisar `problemas_y_propuestas.md` para conocer problemas conocidos y soluciones propuestas.

### Presentación de Propuestas

1. Comenzar con una explicación clara del objetivo y beneficio educativo.
2. Presentar un esquema de la solución antes de implementarla.
3. Explicar cada decisión de diseño y su razonamiento.
4. Ofrecer alternativas cuando sea relevante para fomentar la comprensión.

### Implementación de Código

1. Seguir la estructura de carpetas existente.
2. Incluir docstrings completos en cada función, clase o método.
3. Mantener un estilo de código consistente con el resto del proyecto.
4. Evitar dependencias innecesarias que compliquen la comprensión.

### Documentación de Cambios

Solo cuando el usuario lo solicite explícitamente:

1. Actualizar `process.md` con una entrada que incluya fecha y resumen de cambios.
2. Actualizar `grimorio-proyecto.md` si se añade una nueva funcionalidad.
3. Crear o actualizar documentos de integración específicos (`integracion_*.md`).
4. Documentar problemas encontrados en `problemas_y_propuestas.md`.

## Formato de Mensajes

1. **Claridad sobre complejidad**: Explicar conceptos de manera accesible.
2. **Estructura progresiva**: Presentar información de manera gradual, de lo general a lo específico.
3. **Código comentado**: Incluir comentarios explicativos en bloques de código.
4. **Opciones educativas**: Presentar alternativas para fomentar la comprensión y el criterio técnico.

---

Este documento sirve como guía para los agentes de IA que trabajan en el repositorio MetanoIA. Su propósito es asegurar que todas las contribuciones mantengan la filosofía educativa del proyecto y sigan las convenciones establecidas.
