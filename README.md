# Actividad Semanas 1 y 2: POO, UML, Herencia y Composición

## Datos del estudiante

- Estudiante: Edisson Carchi
- Matrícula: 2025372938
- Asignatura: Programación Orientada a Objetos
- Lenguaje: Python 3.9+
- Repositorio público: https://github.com/Lehendss/sistema-biblioteca-poo

## Caso seleccionado

Se implementó un **sistema de biblioteca**. La biblioteca registra materiales, usuarios y préstamos. El ejemplo permite demostrar encapsulación, getters/setters, herencia y composición sin depender de librerías externas.

## Relacion con la consigna

### Semana 1: clases, objetos, encapsulación y UML

- `Persona` y `Material` son clases base.
- Sus atributos se almacenan como privados usando nombres con doble guion bajo, por ejemplo `__nombre` y `__titulo`.
- Los atributos se consultan y modifican mediante propiedades `@property`, que funcionan como getters y setters.
- `Biblioteca` y `Catálogo` representan objetos que se crean y utilizan desde `main.py`.

### Semana 2: herencia y composición

- `Usuario` y `Bibliotecario` heredan de `Persona`.
- `Libro` y `Revista` heredan de `Material`.
- `Biblioteca` compone un `Catálogo` y una colección de objetos `Préstamo`.
- `Préstamo` compone referencias a un `Usuario` y un `Material`.
- La composición se observa porque el catálogo y los préstamos son administrados por la biblioteca y participan en sus operaciones.

## Estructura

```text
semana1/
├── README.md
├── memoria_entrega_poo.docx
├── docs/
│   ├── diagrama_uml.md
│   └── diagrama_uml.puml
├── src/
│   ├── __init__.py
│   ├── biblioteca.py
│   ├── main.py
│   ├── material.py
│   ├── persona.py
│   └── prestamo.py
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

## Explicación del diseño

`Material` encapsula el estado `disponible`; el código externo no modifica directamente ese atributo. `Libro` y `Revista` reutilizan el comportamiento común de `Material` y agregan datos propios. `Persona` concentra los datos comunes de identificación y contacto, mientras que sus subclases expresan roles distintos.

`Biblioteca` es el punto de coordinación de las operaciones. Su método `prestar` valida usuario y material, cambia el estado del material, crea un `Préstamo` y lo guarda. Su método `devolver` busca el préstamo activo, actualiza la fecha y libera el material. Así se evita que `main.py` manipule directamente las colecciones internas.

## UML

El diagrama completo está en `docs/diagrama_uml.puml` y `docs/diagrama_uml.md`. Relaciones principales:

- Herencia: `Persona <|-- Usuario`, `Persona <|-- Bibliotecario`.
- Herencia: `Material <|-- Libro`, `Material <|-- Revista`.
- Composición: `Biblioteca *-- Catálogo` y `Biblioteca *-- Préstamo`.
- Asociación: `Préstamo --> Usuario` y `Préstamo --> Material`.

## Evidencia y autoría

La memoria en Word presenta la explicación de la solución, los datos del estudiante, el enlace público al repositorio de GitHub y la referencia al diagrama UML. El código fuente, las pruebas y los diagramas se encuentran organizados en este repositorio para su revisión y ejecución.
