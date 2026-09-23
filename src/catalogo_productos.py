from copy import deepcopy
from decimal import Decimal, InvalidOperation
from typing import Dict, List, Set

from .material import Libro, Material, Revista


class Producto:
    """Producto comercial que contiene un material del modelo anterior."""

    def __init__(self, material: Material, precio: str, stock: int) -> None:
        if not isinstance(material, (Libro, Revista)):
            raise ValueError("El producto debe ser un libro o una revista")
        try:
            importe = Decimal(str(precio).replace(",", "."))
        except InvalidOperation:
            raise ValueError("El precio debe ser numérico") from None
        if not importe.is_finite() or importe <= 0:
            raise ValueError("El precio debe ser positivo y finito")
        if importe != importe.quantize(Decimal("0.01")):
            raise ValueError("El precio admite hasta dos decimales")
        if type(stock) is not int or stock < 0:
            raise ValueError("El stock debe ser un entero no negativo")
        self.__material = deepcopy(material)
        self.__precio = importe
        self.__stock = stock

    @property
    def material(self) -> Material:
        return deepcopy(self.__material)

    @property
    def codigo(self) -> str:
        return self.__material.codigo

    @property
    def precio(self) -> Decimal:
        return self.__precio

    @property
    def stock(self) -> int:
        return self.__stock


class CatalogoProductos:
    def __init__(self) -> None:
        self.__productos: Dict[str, Producto] = {}
        self.__codigos: Set[str] = set()
        self.__historial: List[str] = []

    @staticmethod
    def normalizar(codigo: str) -> str:
        return codigo.strip().upper()

    def agregar(self, producto: Producto) -> None:
        codigo = self.normalizar(producto.codigo)
        if codigo in self.__codigos:
            raise ValueError(f"El código {codigo} ya existe")
        self.__productos[codigo] = deepcopy(producto)
        self.__codigos.add(codigo)
        self.__historial.append(f"Creado: {codigo}")

    def buscar(self, codigo: str) -> Producto:
        codigo = self.normalizar(codigo)
        if codigo not in self.__productos:
            raise ValueError(f"No existe el código {codigo}")
        return deepcopy(self.__productos[codigo])

    def listar(self, texto: str = "") -> List[Producto]:
        texto = texto.strip().casefold()
        return [deepcopy(p) for p in self.__productos.values()
                if texto in p.codigo.casefold() or texto in p.material.titulo.casefold()]

    def actualizar(self, codigo: str, producto: Producto) -> None:
        codigo = self.normalizar(codigo)
        self.buscar(codigo)
        if codigo != producto.codigo:
            raise ValueError("El código es la identidad del producto y no se cambia")
        self.__productos[codigo] = deepcopy(producto)
        self.__historial.append(f"Actualizado: {codigo}")

    def eliminar(self, codigo: str) -> None:
        codigo = self.normalizar(codigo)
        self.buscar(codigo)
        del self.__productos[codigo]
        self.__codigos.remove(codigo)
        self.__historial.append(f"Eliminado: {codigo}")

    @property
    def historial(self) -> List[str]:
        return self.__historial.copy()


def catalogo_demo() -> CatalogoProductos:
    catalogo = CatalogoProductos()
    catalogo.agregar(Producto(Libro("L001", "El principito", "Antoine de Saint-Exupéry", "9780156012195"), "15.50", 8))
    catalogo.agregar(Producto(Revista("R001", "Ciencia Hoy", 42), "6.00", 12))
    return catalogo
