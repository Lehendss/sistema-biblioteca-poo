from __future__ import annotations


class Material:
    """Clase base para cualquier material prestable."""

    def __init__(self, codigo: str, titulo: str) -> None:
        self.codigo = codigo
        self.titulo = titulo
        self.disponible = True

    @property
    def codigo(self) -> str:
        return self.__codigo

    @codigo.setter
    def codigo(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise ValueError("El codigo es obligatorio")
        self.__codigo = valor.strip().upper()

    @property
    def titulo(self) -> str:
        return self.__titulo

    @titulo.setter
    def titulo(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise ValueError("El titulo es obligatorio")
        self.__titulo = valor.strip()

    @property
    def disponible(self) -> bool:
        return self.__disponible

    @disponible.setter
    def disponible(self, valor: bool) -> None:
        if not isinstance(valor, bool):
            raise TypeError("disponible debe ser booleano")
        self.__disponible = valor

    def prestar(self) -> None:
        if not self.disponible:
            raise ValueError("El material ya esta prestado")
        self.disponible = False

    def devolver(self) -> None:
        if self.disponible:
            raise ValueError("El material ya se encuentra disponible")
        self.disponible = True

    def descripcion(self) -> str:
        estado = "disponible" if self.disponible else "prestado"
        return f"{self.codigo} - {self.titulo} ({estado})"


class Libro(Material):
    """Material especializado que agrega autor e ISBN."""

    def __init__(self, codigo: str, titulo: str, autor: str, isbn: str) -> None:
        super().__init__(codigo, titulo)
        self.autor = autor
        self.isbn = isbn

    @property
    def autor(self) -> str:
        return self.__autor

    @autor.setter
    def autor(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise ValueError("El autor es obligatorio")
        self.__autor = valor.strip()

    @property
    def isbn(self) -> str:
        return self.__isbn

    @isbn.setter
    def isbn(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise ValueError("El ISBN es obligatorio")
        self.__isbn = valor.strip()

    def descripcion(self) -> str:
        return f"Libro: {super().descripcion()} - Autor: {self.autor}"


class Revista(Material):
    """Material especializado que agrega numero de edicion."""

    def __init__(self, codigo: str, titulo: str, numero_edicion: int) -> None:
        super().__init__(codigo, titulo)
        self.numero_edicion = numero_edicion

    @property
    def numero_edicion(self) -> int:
        return self.__numero_edicion

    @numero_edicion.setter
    def numero_edicion(self, valor: int) -> None:
        if not isinstance(valor, int) or valor <= 0:
            raise ValueError("El numero de edicion debe ser positivo")
        self.__numero_edicion = valor

    def descripcion(self) -> str:
        return f"Revista: {super().descripcion()} - Edicion: {self.numero_edicion}"
