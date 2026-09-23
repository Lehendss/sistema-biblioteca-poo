import argparse
import flet as ft

from .catalogo_productos import Producto, catalogo_demo
from .material import Libro, Revista


def main(page: ft.Page):
    page.title = "Biblioteca | Catálogo de productos"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 24
    page.bgcolor = "#F3F6FA"
    page.scroll = ft.ScrollMode.AUTO
    catalogo = catalogo_demo()
    seleccionado = None

    codigo = ft.TextField(label="Código", width=200)
    titulo = ft.TextField(label="Título", width=400)
    tipo = ft.Dropdown(label="Tipo", value="Libro", width=180,
                       options=[ft.dropdown.Option("Libro"), ft.dropdown.Option("Revista")])
    autor = ft.TextField(label="Autor", width=280)
    isbn = ft.TextField(label="ISBN", width=220)
    edicion = ft.TextField(label="Edición", value="1", width=140, visible=False)
    precio = ft.TextField(label="Precio ($)", width=180)
    stock = ft.TextField(label="Stock", width=140)
    for campo in [codigo, titulo, autor, isbn, edicion, precio, stock]:
        campo.on_change = lambda e: None
    filtro = ft.TextField(label="Buscar por código o título", width=460)
    mensaje = ft.Text("Seleccione un producto o complete el formulario para agregar uno.", color="#164E63")
    resumen = ft.Text()
    historial = ft.Text(size=12)
    tabla = ft.DataTable(columns=[ft.DataColumn(ft.Text(t)) for t in
                         ["Código", "Producto", "Tipo", "Precio", "Stock", "Acción"]], rows=[])

    def avisar(texto, error=False):
        mensaje.value = texto
        mensaje.color = "#B91C1C" if error else "#166534"

    def cambiar_tipo(e=None):
        autor.visible = isbn.visible = tipo.value == "Libro"
        edicion.visible = tipo.value == "Revista"
        page.update()

    def refrescar(e=None):
        tabla.rows.clear()
        productos = catalogo.listar(filtro.value or "")
        for p in productos:
            m = p.material
            tabla.rows.append(ft.DataRow(cells=[
                ft.DataCell(ft.Text(p.codigo)), ft.DataCell(ft.Text(m.titulo)),
                ft.DataCell(ft.Text("Libro" if isinstance(m, Libro) else "Revista")),
                ft.DataCell(ft.Text(f"${p.precio:.2f}")), ft.DataCell(ft.Text(str(p.stock))),
                ft.DataCell(ft.TextButton("Editar " + p.codigo,
                            on_click=lambda e, c=p.codigo: seleccionar(c)))]))
        resumen.value = f"{len(productos)} resultados · {len(catalogo.listar())} productos en el catálogo"
        historial.value = "Últimas operaciones: " + " | ".join(catalogo.historial[-4:])
        page.update()

    def limpiar(e=None):
        nonlocal seleccionado
        seleccionado = None
        codigo.disabled = False
        for campo in [codigo, titulo, autor, isbn, precio, stock]:
            campo.value = ""
        tipo.value = "Libro"
        edicion.value = "1"
        actualizar.disabled = eliminar.disabled = True
        agregar.disabled = False
        cambiar_tipo()

    def seleccionar(c):
        nonlocal seleccionado
        p = catalogo.buscar(c)
        m = p.material
        seleccionado = c
        codigo.value, titulo.value = c, m.titulo
        codigo.disabled = True
        precio.value, stock.value = str(p.precio), str(p.stock)
        tipo.value = "Libro" if isinstance(m, Libro) else "Revista"
        if isinstance(m, Libro):
            autor.value, isbn.value = m.autor, m.isbn
        else:
            edicion.value = str(m.numero_edicion)
        actualizar.disabled = eliminar.disabled = False
        agregar.disabled = True
        avisar(f"Producto {c} cargado para edición.")
        cambiar_tipo()

    def producto_formulario():
        if not (codigo.value or "").strip() or not (titulo.value or "").strip():
            raise ValueError("Código y título son obligatorios")
        try:
            unidades = int(stock.value)
        except (ValueError, TypeError):
            raise ValueError("El stock debe ser un entero no negativo") from None
        if tipo.value == "Libro":
            if not (autor.value or "").strip() or not (isbn.value or "").strip():
                raise ValueError("Autor e ISBN son obligatorios para un libro")
            material = Libro(codigo.value, titulo.value, autor.value, isbn.value)
        else:
            try:
                numero = int(edicion.value)
            except (ValueError, TypeError):
                raise ValueError("La edición debe ser un entero positivo") from None
            if numero <= 0:
                raise ValueError("La edición debe ser un entero positivo")
            material = Revista(codigo.value, titulo.value, numero)
        return Producto(material, precio.value, unidades)

    def guardar(e, editar=False):
        try:
            p = producto_formulario()
            if editar:
                catalogo.actualizar(seleccionado, p)
            else:
                catalogo.agregar(p)
            limpiar()
            avisar(f"Producto {p.codigo} {'actualizado' if editar else 'agregado'} correctamente.")
        except ValueError as error:
            avisar(str(error), True)
        refrescar()

    def borrar(e):
        try:
            c = seleccionado
            catalogo.eliminar(c)
            limpiar()
            avisar(f"Producto {c} eliminado correctamente.")
        except ValueError as error:
            avisar(str(error), True)
        refrescar()

    agregar = ft.ElevatedButton("Agregar", on_click=guardar)
    actualizar = ft.ElevatedButton("Actualizar", disabled=True, on_click=lambda e: guardar(e, True))
    eliminar = ft.OutlinedButton("Eliminar", disabled=True, on_click=borrar)
    tipo.on_change = cambiar_tipo
    filtro.on_change = refrescar
    filtro.on_submit = refrescar
    page.add(
        ft.Text("Catálogo de productos", size=30, weight=ft.FontWeight.BOLD, color="#17365D"),
        ft.Text("Biblioteca · Semanas 5 y 6 · Edisson Carchi", size=16),
        ft.Text("Libros y revistas del modelo anterior. Datos de demostración en memoria; se reinician al abrir una sesión."),
        ft.Container(ft.Column([
            ft.Row([codigo, titulo, tipo], wrap=True), ft.Row([autor, isbn, edicion], wrap=True),
            ft.Row([precio, stock], wrap=True),
            ft.Row([agregar, actualizar, eliminar, ft.TextButton("Nuevo / limpiar", on_click=limpiar)], wrap=True),
            mensaje]), padding=20, bgcolor="white", border_radius=12),
        ft.Row([filtro, ft.OutlinedButton("Listar / buscar", on_click=refrescar)], wrap=True),
        resumen, ft.Row([tabla], scroll=ft.ScrollMode.AUTO), historial)
    refrescar()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--web", action="store_true")
    parser.add_argument("--port", type=int, default=8550)
    args = parser.parse_args()
    ft.app(target=main, view=ft.AppView.WEB_BROWSER if args.web else ft.AppView.FLET_APP,
           port=args.port if args.web else 0, host="127.0.0.1")
