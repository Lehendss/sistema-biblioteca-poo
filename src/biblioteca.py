from __future__ import annotations

from typing import Dict, List

from .material import Material
from .persona import Usuario
from .prestamo import Prestamo


class Catalogo:
    """Componente compuesto por la biblioteca para administrar materiales."""

    def __init__(self) -> None:
        self.__materiales: Dict[str, Material] = {}

    @property
    def materiales(self) -> tuple:
        return tuple(self.__materiales.values())

    def agregar(self, material: Material) -> None:
        if material.codigo in self.__materiales:
            raise ValueError("Ya existe un material con ese codigo")
        self.__materiales[material.codigo] = material

    def buscar(self, codigo: str) -> Material:
        try:
            return self.__materiales[codigo.upper()]
        except KeyError as error:
            raise ValueError("Material no encontrado") from error


class Biblioteca:
    """Fachada del sistema y composicion de catalogo y prestamos."""

    def __init__(self, nombre: str) -> None:
        if not nombre or not nombre.strip():
            raise ValueError("El nombre de la biblioteca es obligatorio")
        self.__nombre = nombre.strip()
        self.__catalogo = Catalogo()
        self.__usuarios: Dict[str, Usuario] = {}
        self.__prestamos: List[Prestamo] = []

    @property
    def nombre(self) -> str:
        return self.__nombre

    @property
    def catalogo(self) -> Catalogo:
        return self.__catalogo

    @property
    def prestamos(self) -> tuple:
        return tuple(self.__prestamos)

    def registrar_material(self, material: Material) -> None:
        self.__catalogo.agregar(material)

    def registrar_usuario(self, usuario: Usuario) -> None:
        if usuario.identificacion in self.__usuarios:
            raise ValueError("El usuario ya esta registrado")
        self.__usuarios[usuario.identificacion] = usuario

    def prestar(self, codigo_material: str, identificacion_usuario: str) -> Prestamo:
        material = self.__catalogo.buscar(codigo_material)
        try:
            usuario = self.__usuarios[identificacion_usuario]
        except KeyError as error:
            raise ValueError("Usuario no encontrado") from error

        material.prestar()
        prestamo = Prestamo(usuario, material)
        self.__prestamos.append(prestamo)
        usuario.agregar_prestamo(prestamo)
        return prestamo

    def devolver(self, codigo_material: str) -> Prestamo:
        material = self.__catalogo.buscar(codigo_material)
        for prestamo in reversed(self.__prestamos):
            if prestamo.material.codigo == material.codigo and prestamo.activo:
                prestamo.cerrar()
                material.devolver()
                return prestamo
        raise ValueError("No existe un prestamo activo para ese material")
