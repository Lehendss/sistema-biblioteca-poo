from __future__ import annotations

from .cliente import Cliente


class Venta:
    """Composicion de una operacion con un cliente polimorfico."""

    def __init__(self, cliente: Cliente, subtotal: float) -> None:
        if subtotal < 0:
            raise ValueError("El subtotal no puede ser negativo")
        self.__cliente = cliente
        self.__subtotal = round(subtotal, 2)

    @property
    def cliente(self) -> Cliente:
        return self.__cliente

    @property
    def subtotal(self) -> float:
        return self.__subtotal

    @property
    def descuento(self) -> float:
        return self.cliente.calcular_descuento(self.subtotal)

    @property
    def total(self) -> float:
        return round(self.subtotal - self.descuento, 2)
