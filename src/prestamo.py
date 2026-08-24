from __future__ import annotations

from datetime import date
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .material import Material
    from .persona import Usuario


class Prestamo:
    """Relacion entre un usuario y un material durante un periodo."""

    def __init__(self, usuario: Usuario, material: Material) -> None:
        self.__usuario = usuario
        self.__material = material
        self.__fecha_prestamo = date.today()
        self.__fecha_devolucion: Optional[date] = None

    @property
    def usuario(self) -> Usuario:
        return self.__usuario

    @property
    def material(self) -> Material:
        return self.__material

    @property
    def fecha_prestamo(self) -> date:
        return self.__fecha_prestamo

    @property
    def fecha_devolucion(self) -> Optional[date]:
        return self.__fecha_devolucion

    @property
    def activo(self) -> bool:
        return self.__fecha_devolucion is None

    def cerrar(self) -> None:
        if not self.activo:
            raise ValueError("El prestamo ya fue cerrado")
        self.__fecha_devolucion = date.today()
