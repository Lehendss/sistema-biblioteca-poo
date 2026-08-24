# Actividad Semanas 1 y 2: POO, UML, Herencia y Composición

## Datos del estudiante

- Estudiante: `[COMPLETAR]`
- Matricula: `[COMPLETAR]`
- Asignatura: Programacion Orientada a Objetos
- Lenguaje: Python 3.9+
- Repositorio publico: https://github.com/Lehendss/sistema-biblioteca-poo

## Caso seleccionado

Se implemento un **sistema de biblioteca**. La biblioteca registra materiales, usuarios y prestamos. El ejemplo permite demostrar encapsulacion, getters/setters, herencia y composicion sin depender de librerias externas.

## Relacion con la consigna

### Semana 1: clases, objetos, encapsulacion y UML

- `Persona` y `Material` son clases base.
- Sus atributos se almacenan como privados usando nombres con doble guion bajo, por ejemplo `__nombre` y `__titulo`.
- Los atributos se consultan y modifican mediante propiedades `@property`, que funcionan como getters y setters.
- `Biblioteca` y `Catalogo` representan objetos que se crean y utilizan desde `main.py`.

### Semana 2: herencia y composicion

- `Usuario` y `Bibliotecario` heredan de `Persona`.
- `Libro` y `Revista` heredan de `Material`.
- `Biblioteca` compone un `Catalogo` y una coleccion de objetos `Prestamo`.
- `Prestamo` compone referencias a un `Usuario` y un `Material`.
- La composicion se observa porque el catalogo y los prestamos son administrados por la biblioteca y participan en sus operaciones.

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

## Ejecucion

Desde la carpeta `semana1`:

```bash
python3 -m src.main
python3 -m unittest discover -s tests -v
```

No se requieren paquetes externos.

## Funcionamiento esperado

1. Se crea una biblioteca.
2. Se agregan un libro y una revista al catalogo.
3. Se registra un usuario y un bibliotecario.
4. El usuario solicita el libro.
5. La biblioteca crea un prestamo y marca el material como no disponible.
6. Se devuelve el libro y vuelve a estar disponible.
7. Se intenta devolverlo nuevamente para demostrar el control de errores.

## Explicacion de diseno

`Material` encapsula el estado `disponible`; el codigo externo no modifica directamente ese atributo. `Libro` y `Revista` reutilizan el comportamiento comun de `Material` y agregan datos propios. `Persona` concentra los datos comunes de identificacion y contacto, mientras que sus subclases expresan roles distintos.

`Biblioteca` es el punto de coordinacion de las operaciones. Su metodo `prestar` valida usuario y material, cambia el estado del material, crea un `Prestamo` y lo guarda. Su metodo `devolver` busca el prestamo activo, actualiza la fecha y libera el material. Asi se evita que `main.py` manipule directamente las colecciones internas.

## UML

El diagrama completo esta en `docs/diagrama_uml.puml` y `docs/diagrama_uml.md`. Relaciones principales:

- Herencia: `Persona <|-- Usuario`, `Persona <|-- Bibliotecario`.
- Herencia: `Material <|-- Libro`, `Material <|-- Revista`.
- Composicion: `Biblioteca *-- Catalogo` y `Biblioteca *-- Prestamo`.
- Asociacion: `Prestamo --> Usuario` y `Prestamo --> Material`.

## Evidencia y autoria

La memoria Word contiene esta explicacion, el enlace de GitHub como campo editable y el UML en formato fuente. Antes de entregar, el estudiante debe publicar el codigo en un repositorio propio, reemplazar los campos pendientes y conservar commits que pueda explicar.
