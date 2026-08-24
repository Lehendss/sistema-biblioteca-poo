import unittest

from src.biblioteca import Biblioteca
from src.material import Libro, Revista
from src.persona import Usuario


class BibliotecaTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.biblioteca = Biblioteca("Biblioteca de prueba")
        self.libro = Libro("l001", "Libro de prueba", "Autor de prueba", "ISBN-001")
        self.usuario = Usuario("u001", "Usuario de prueba", "usuario@example.com")
        self.biblioteca.registrar_material(self.libro)
        self.biblioteca.registrar_material(Revista("r001", "Revista de prueba", 1))
        self.biblioteca.registrar_usuario(self.usuario)

    def test_encapsulacion_normaliza_codigo(self) -> None:
        self.assertEqual("L001", self.libro.codigo)
        self.libro.titulo = "  Nuevo titulo  "
        self.assertEqual("Nuevo titulo", self.libro.titulo)

    def test_herencia_de_materiales(self) -> None:
        self.assertIsInstance(self.libro, Libro)
        self.assertTrue(hasattr(self.libro, "prestar"))

    def test_prestamo_y_devolucion(self) -> None:
        prestamo = self.biblioteca.prestar("L001", "u001")
        self.assertTrue(prestamo.activo)
        self.assertFalse(self.libro.disponible)
        self.assertEqual(1, len(self.usuario.prestamos))

        self.biblioteca.devolver("L001")
        self.assertFalse(prestamo.activo)
        self.assertTrue(self.libro.disponible)

    def test_no_se_puede_prestar_dos_veces(self) -> None:
        self.biblioteca.prestar("L001", "u001")
        with self.assertRaises(ValueError):
            self.biblioteca.prestar("L001", "u001")

    def test_validacion_de_datos(self) -> None:
        with self.assertRaises(ValueError):
            Usuario("", "Nombre", "nombre@example.com")
        with self.assertRaises(ValueError):
            Libro("L002", "Titulo", "Autor", "")


if __name__ == "__main__":
    unittest.main()
