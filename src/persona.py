from __future__ import annotations

from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from .prestamo import Prestamo


class Persona:
    """Clase base que encapsula los datos comunes de una persona."""

    def __init__(self, identificacion: str, nombre: str, correo: str) -> None:
        self.identificacion = identificacion
        self.nombre = nombre
        self.correo = correo

    @property
    def identificacion(self) -> str:
        return self.__identificacion

    @identificacion.setter
    def identificacion(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise ValueError("La identificacion es obligatoria")
        self.__identificacion = valor.strip()

    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise ValueError("El nombre es obligatorio")
        self.__nombre = valor.strip()

    @property
    def correo(self) -> str:
        return self.__correo

    @correo.setter
    def correo(self, valor: str) -> None:
        if "@" not in valor:
            raise ValueError("El correo debe contener @")
        self.__correo = valor.strip()

    def descripcion(self) -> str:
        return f"{self.nombre} ({self.identificacion})"


class Usuario(Persona):
    """Persona que puede solicitar materiales."""

    def __init__(self, identificacion: str, nombre: str, correo: str) -> None:
        super().__init__(identificacion, nombre, correo)
        self.__prestamos: List[Prestamo] = []

    @property
    def prestamos(self) -> tuple:
        """Devuelve una vista inmutable de los prestamos del usuario."""
        return tuple(self.__prestamos)

    def agregar_prestamo(self, prestamo: Prestamo) -> None:
        self.__prestamos.append(prestamo)


class Bibliotecario(Persona):
    """Persona responsable de administrar la biblioteca."""

    def registrar_material(self, biblioteca: object, material: object) -> None:
        biblioteca.registrar_material(material)
