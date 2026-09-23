# Semanas 5 y 6: catálogo e interfaz gráfica

**Estudiante:** Edisson Carchi · **Matrícula:** 2025372938

## Instalación y ejecución

Desde la raíz del repositorio, con Python 3.10 o superior (verificado en 3.12):

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m src.gui
```

En Windows se activa con `.venv\Scripts\activate`. Para abrir la misma interfaz Flet en el navegador:

```bash
python -m src.gui --web --port 8550
```

La dirección es http://127.0.0.1:8550. Los datos viven en memoria por sesión: al cerrar y volver a abrir se cargan los dos productos iniciales. No se requiere base de datos.

## Uso

1. Completar código, título, tipo, precio, stock y los datos específicos del libro o revista. Pulsar **Agregar**.
2. Escribir un código o título en el buscador para filtrar; vaciarlo lista todo.
3. Pulsar **Editar CÓDIGO** para consultar y cargar los datos en el formulario.
4. Modificar campos y pulsar **Actualizar**. El código no cambia porque identifica el producto.
5. Pulsar **Eliminar** sobre un producto seleccionado.
6. **Nuevo / limpiar** habilita el formulario para otra alta.

## Colecciones e integración

- `dict[str, Producto]`: índice privado que permite buscar, actualizar y eliminar por código.
- `set[str]`: códigos normalizados para rechazar duplicados, incluso con distinta capitalización o espacios.
- `list[str]`: historial ordenado de operaciones exitosas. `listar()` devuelve además una lista filtrada de productos.
- `Producto` contiene un `Libro` o `Revista`, clases heredadas de `Material` de las semanas anteriores. Agrega precio y stock con validación. Las copias protegen el estado interno frente a mutaciones externas.
- Se usan anotaciones de tipos para documentar las colecciones; en Python no sustituyen la validación en ejecución. La consigna exige genéricos explícitos únicamente en Java.
- Los eventos `on_click`, `on_change` y `on_submit` conectan los controles con el catálogo. Cada operación actualiza tabla, historial y mensajes.
- Se admiten precios positivos con dos decimales, stock entero no negativo y edición positiva. Autor e ISBN son obligatorios para libros; código y título siempre son obligatorios. La regla de duplicidad es el código, no el título ni el ISBN.

## Verificación

```bash
python -m unittest discover -s tests -v
```

El repositorio completo incluye las clases anteriores y esta extensión. La memoria de entrega se genera con `tools/generar_memoria56.py` y contiene las capturas reales guardadas en `capturas/`.

Repositorio: https://github.com/Lehendss/sistema-biblioteca-poo

Entrega en Blackboard: convertir `Carchi_Edisson_Semanas5y6.docx` a PDF. El PDF contiene datos, explicación, capturas y enlace al repositorio.
