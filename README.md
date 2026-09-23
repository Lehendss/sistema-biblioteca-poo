# Actividad Semanas 1 y 2: POO, UML, Herencia y Composición

## Semanas 5 y 6: catálogo gráfico con Flet

La nueva interfaz reutiliza `Libro` y `Revista` y permite agregar, buscar, listar, actualizar y eliminar productos. Usa `dict`, `set` y `list`, validaciones y manejo de eventos.

Con Python 3.10+ (probado en 3.12), desde la raíz del repositorio:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m src.gui
```

En Windows: `.venv\Scripts\activate`. Versión web: `python -m src.gui --web --port 8550`.

Consulta las [instrucciones de las semanas 5 y 6](entregas/semanas5y6/README.md) para conocer el uso, las colecciones y la entrega. Los datos son de demostración y se conservan en memoria durante cada sesión.

## Datos del estudiante

- Estudiante: Edisson Carchi
- Matrícula: 2025372938
- Asignatura: Programación Orientada a Objetos
- Lenguaje: Python 3.9+
- Repositorio público: https://github.com/Lehendss/sistema-biblioteca-poo

## Caso seleccionado

Se implementó un **sistema de biblioteca**. La biblioteca registra materiales, usuarios y préstamos. El ejemplo permite demostrar encapsulación, getters/setters, herencia y composición sin depender de librerías externas.

## Relación con la consigna

### Semana 1: clases, objetos, encapsulación y UML

- `Persona` y `Material` son clases base.
- Sus atributos se almacenan como privados usando nombres con doble guión bajo, por ejemplo `__nombre` y `__titulo`.
- Los atributos se consultan y modifican mediante propiedades `@property`, que funcionan como getters y setters.
- `Biblioteca` y `Catálogo` representan objetos que se crean y utilizan desde `main.py`.

### Semana 2: herencia y composición

- `Usuario` y `Bibliotecario` heredan de `Persona`.
- `Libro` y `Revista` heredan de `Material`.
- `Biblioteca` compone un `Catálogo` y una colección de objetos `Préstamo`.
- `Préstamo` compone referencias a un `Usuario` y un `Material`.
- La composición se observa porque el catálogo y los préstamos son administrados por la biblioteca y participan en sus operaciones.

### Semana 3: polimorfismo, interfaces y clases abstractas

- `Cliente` es una clase abstracta de Python (`ABC`) que declara `calcular_descuento()`.
- `ClienteMayorista` y `ClienteMinorista` heredan de `Cliente` y sobrescriben ese método con reglas distintas.
- `Venta` recibe cualquier objeto `Cliente` y calcula `descuento` mediante la abstracción común, sin identificar el tipo concreto.
- Reglas utilizadas: mayorista 15 % desde 1000 y 10 % por debajo; minorista 5 % desde 500 y 0 % por debajo.

## Estructura

```text
semana1/
├── README.md
├── memoria_entrega_poo.docx
├── memoria_entrega_poo.html
├── docs/
│   ├── diagrama_uml.md
│   └── diagrama_uml.puml
├── src/
│   ├── __init__.py
│   ├── biblioteca.py
│   ├── cliente.py
│   ├── main.py
│   ├── material.py
│   ├── persona.py
│   ├── prestamo.py
│   └── venta.py
└── tests/
    └── test_biblioteca.py
```

## Ejecución

Desde la carpeta `semana1`:

```bash
python3 -m src.main
python3 -m unittest discover -s tests -v
```

No se requieren paquetes externos.

## Funcionamiento esperado

1. Se crea una biblioteca.
2. Se agregan un libro y una revista al catálogo.
3. Se registra un usuario y un bibliotecario.
4. El usuario solicita el libro.
5. La biblioteca crea un préstamo y marca el material como no disponible.
6. Se devuelve el libro y vuelve a estar disponible.
7. Se intenta devolverlo nuevamente para demostrar el control de errores.
8. Se calculan ventas para clientes mayoristas y minoristas usando la misma operación polimórfica.

## Explicación del diseño

`Material` encapsula el estado `disponible`; el código externo no modifica directamente ese atributo. `Libro` y `Revista` reutilizan el comportamiento común de `Material` y agregan datos propios. `Persona` concentra los datos comunes de identificación y contacto, mientras que sus subclases expresan roles distintos.

`Biblioteca` es el punto de coordinación de las operaciones. Su método `prestar` valida usuario y material, cambia el estado del material, crea un `Préstamo` y lo guarda. Su método `devolver` busca el préstamo activo, actualiza la fecha y libera el material. Así se evita que `main.py` manipule directamente las colecciones internas.

En la extensión de la semana 3, `Venta` trabaja con una referencia de tipo `Cliente`. Al solicitar `venta.descuento`, Python ejecuta automáticamente la versión sobrescrita correspondiente al objeto real. La misma operación funciona para `ClienteMayorista` y `ClienteMinorista`, lo que demuestra polimorfismo y evita condicionales para identificar tipos.

## UML

El diagrama completo está en `docs/diagrama_uml.puml` y `docs/diagrama_uml.md`. Relaciones principales:

- Herencia: `Persona <|-- Usuario`, `Persona <|-- Bibliotecario`.
- Herencia: `Material <|-- Libro`, `Material <|-- Revista`.
- Composición: `Biblioteca *-- Catálogo` y `Biblioteca *-- Préstamo`.
- Asociación: `Préstamo --> Usuario` y `Préstamo --> Material`.
- Abstracción y polimorfismo: `Cliente` define `calcular_descuento()` y sus subclases lo sobrescriben.
- Composición: `Venta` contiene una referencia a la abstracción `Cliente`.

## Evidencia y autoría

La memoria en Word presenta la explicación de la solución, los datos del estudiante, el enlace público al repositorio de GitHub y la referencia al diagrama UML. El código fuente, las pruebas y los diagramas se encuentran organizados en este repositorio para su revisión y ejecución.
