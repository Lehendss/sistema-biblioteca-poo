from __future__ import annotations

from abc import ABC, abstractmethod


class Cliente(ABC):
    """Abstraccion comun para clientes con reglas de descuento."""

    def __init__(self, identificacion: str, nombre: str) -> None:
        self.identificacion = identificacion
        self.nombre = nombre

    @property
    def identificacion(self) -> str:
        return self.__identificacion

    @identificacion.setter
    def identificacion(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise ValueError("La identificacion del cliente es obligatoria")
        self.__identificacion = valor.strip()

    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise ValueError("El nombre del cliente es obligatorio")
        self.__nombre = valor.strip()

    @abstractmethod
    def calcular_descuento(self, subtotal: float) -> float:
        """Devuelve el valor monetario del descuento aplicable."""
        raise NotImplementedError

    def validar_subtotal(self, subtotal: float) -> None:
        if subtotal < 0:
            raise ValueError("El subtotal no puede ser negativo")


class ClienteMayorista(Cliente):
    """Cliente que compra por volumen y recibe descuentos escalonados."""

    def calcular_descuento(self, subtotal: float) -> float:
        self.validar_subtotal(subtotal)
        porcentaje = 0.15 if subtotal >= 1000 else 0.10
        return round(subtotal * porcentaje, 2)


class ClienteMinorista(Cliente):
    """Cliente final con descuento por alcanzar un umbral de compra."""

    def calcular_descuento(self, subtotal: float) -> float:
        self.validar_subtotal(subtotal)
        porcentaje = 0.05 if subtotal >= 500 else 0.0
        return round(subtotal * porcentaje, 2)
