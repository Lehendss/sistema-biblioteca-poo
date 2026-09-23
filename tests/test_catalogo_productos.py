import unittest
from decimal import Decimal
from src.catalogo_productos import CatalogoProductos, Producto
from src.material import Libro, Revista


class CatalogoProductosTests(unittest.TestCase):
    def setUp(self):
        self.catalogo = CatalogoProductos()
        self.libro = Producto(Libro(" l01 ", "Título", "Autor", "ISBN"), "12.50", 3)

    def test_crud_y_reutilizacion_codigo(self):
        self.catalogo.agregar(self.libro)
        self.assertEqual(self.catalogo.buscar("l01").stock, 3)
        nuevo = Producto(Revista("L01", "Ciencia", 2), "6.00", 0)
        self.catalogo.actualizar("l01", nuevo)
        self.assertEqual(self.catalogo.buscar("L01").precio, Decimal("6.00"))
        self.assertEqual(len(self.catalogo.listar("ciencia")), 1)
        self.catalogo.eliminar("l01")
        self.assertEqual(self.catalogo.listar(), [])
        self.catalogo.agregar(self.libro)
        self.assertEqual(len(self.catalogo.historial), 4)

    def test_duplicado_no_modifica_estado(self):
        self.catalogo.agregar(self.libro)
        with self.assertRaises(ValueError):
            self.catalogo.agregar(self.libro)
        self.assertEqual(len(self.catalogo.listar()), 1)
        self.assertEqual(len(self.catalogo.historial), 1)

    def test_inexistentes(self):
        for accion in [lambda: self.catalogo.buscar("X"), lambda: self.catalogo.eliminar("X"),
                       lambda: self.catalogo.actualizar("X", self.libro)]:
            with self.assertRaises(ValueError):
                accion()

    def test_copias_protegen_catalogo(self):
        self.catalogo.agregar(self.libro)
        self.catalogo.buscar("L01").material.codigo = "OTRO"
        self.catalogo.listar().clear()
        self.catalogo.historial.clear()
        self.assertEqual(self.catalogo.buscar("L01").codigo, "L01")
        self.assertEqual(len(self.catalogo.historial), 1)

    def test_validaciones(self):
        for precio in ["0", "-1", "abc", "NaN", "Infinity", "1.234"]:
            with self.subTest(precio=precio), self.assertRaises(ValueError):
                Producto(self.libro.material, precio, 2)
        for stock in [-1, 1.5, True]:
            with self.subTest(stock=stock), self.assertRaises(ValueError):
                Producto(self.libro.material, "1.00", stock)

    def test_cambio_identidad_rechazado(self):
        self.catalogo.agregar(self.libro)
        with self.assertRaises(ValueError):
            self.catalogo.actualizar("L01", Producto(Revista("R02", "Revista", 1), "1", 2))
        self.assertEqual(self.catalogo.buscar("L01").stock, 3)
