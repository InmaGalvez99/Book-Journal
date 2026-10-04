**MI RINCÓN DE LECTURA**
Un santuario digital para controlar mis lecturas, dominar mi wishlist infinita y sobrevivir al caos de Goodreads con un poco de magia de código.

Tener visualmente todos los libros leídos, filtrarlos por puntuación, autoras o género de forma clara y atractiva es el sueño de cualquier lector. 
Y pensándolo bien, ¿qué mejor forma de conseguirlo que usando mis conocimientos en Power BI y aprovechando para sumarle Python y SQL y explotar los datos al máximo?

Este proyecto nace para crear un Book Journal completamente personalizado y automatizado, 
combinando el desarrollo técnico con la pasión por tener la biblioteca perfectamente organizada.


**🛠 El Arsenal Tecnológico**
Para montar este pipeline de datos de principio a fin, utilizo una combinación de herramientas clave:

[x] Python (Pandas): Para la automatización del preprocesamiento, limpieza de datos, extracción de sagas y clasificación automatizada por autor.

[x] SQL: Como base de datos relacional para almacenar de forma persistente la información limpia.

[x] Power BI: Para diseñar un informe interactivo, visual y profesional donde exprimir al máximo las métricas de lectura.


**✨ Automatización y Flujo de Datos**
La estantería es un entorno dinámico donde constantemente entran nuevas incorporaciones a la wishlist y se actualizan lecturas. Para evitar procesos manuales repetitivos, el flujo está diseñado de forma automatizada:

1. Ingesta de datos: Exportación de la base de datos de libros en formato CSV.

2. Transformación (Python): El script se encarga de limpiar columnas innecesarias, formatear textos, estructurar sagas y asignar categorías mediante mapeo de diccionarios (etiquetando las nuevas entradas automáticamente para su revisión).

3. Persistencia (SQL): El DataFrame limpio se descarga directamente en la base de datos.

4. Visualización (Power BI): Conexión directa a SQL para actualizar las métricas de rendimiento con un solo clic.


¡Y eso es todo! Si te gusta el proyecto, te robas alguna idea o simplemente quieres cotillear, ¡disfruta del rincón! ☕📚
