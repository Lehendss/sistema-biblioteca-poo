from .biblioteca import Biblioteca
from .cliente import ClienteMayorista, ClienteMinorista
from .material import Libro, Revista
from .persona import Bibliotecario, Usuario
from .venta import Venta


def ejecutar_demo() -> None:
    biblioteca = Biblioteca("Biblioteca Central")
    libro = Libro("L001", "El principito", "Antoine de Saint-Exupery", "978-0156012195")
    revista = Revista("R001", "Ciencia Hoy", 42)
    usuario = Usuario("U001", "Ana Perez", "ana@example.com")
    bibliotecario = Bibliotecario("B001", "Carlos Ruiz", "carlos@example.com")

    bibliotecario.registrar_material(biblioteca, libro)
    bibliotecario.registrar_material(biblioteca, revista)
    biblioteca.registrar_usuario(usuario)

    print(f"Biblioteca: {biblioteca.nombre}")
    for material in biblioteca.catalogo.materiales:
        print(material.descripcion())

    prestamo = biblioteca.prestar("L001", "U001")
    print(f"Prestamo activo: {prestamo.material.titulo} para {prestamo.usuario.nombre}")
    print(f"Disponible despues del prestamo: {libro.disponible}")

    biblioteca.devolver("L001")
    print(f"Disponible despues de la devolucion: {libro.disponible}")

    try:
        biblioteca.devolver("L001")
    except ValueError as error:
        print(f"Control de error: {error}")

    print("\nCalculo polimorfico de descuentos:")
    ventas = (
        Venta(ClienteMayorista("M001", "Distribuidora Andina"), 1500),
        Venta(ClienteMinorista("C001", "Maria Lopez"), 600),
        Venta(ClienteMinorista("C002", "Pedro Gomez"), 200),
    )
    for venta in ventas:
        print(
            f"{venta.cliente.nombre}: subtotal=${venta.subtotal:.2f}, "
            f"descuento=${venta.descuento:.2f}, total=${venta.total:.2f}"
        )


if __name__ == "__main__":
    ejecutar_demo()
