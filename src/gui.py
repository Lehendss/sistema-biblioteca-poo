import argparse

import flet as ft

from .catalogo_productos import Producto, catalogo_demo
from .material import Libro, Revista

HEADER_BG = "#24292F"
HEADER_TEXT = "#FFFFFF"
CANVAS = "#F6F8FA"
SURFACE = "#FFFFFF"
BORDER = "#D0D7DE"
TEXT = "#1F2328"
MUTED = "#656D76"
ACCENT = "#0969DA"
SUCCESS = "#1A7F37"
DANGER = "#CF222E"


def main(page: ft.Page):
    page.title = "Catálogo"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = CANVAS
    page.padding = 0
    page.scroll = ft.ScrollMode.AUTO
    page.theme = ft.Theme(font_family="-apple-system, BlinkMacSystemFont, Segoe UI, Helvetica, Arial, sans-serif")
    page.window_width = 1280
    page.window_height = 800
    page.window_min_width = 900
    page.window_min_height = 600

    catalogo = catalogo_demo()
    seleccionado = None

    def input_field(label, ancho, **kwargs):
        return ft.TextField(
            label=label,
            width=ancho,
            bgcolor=SURFACE,
            border_color=BORDER,
            focused_border_color=ACCENT,
            color=TEXT,
            text_size=13,
            label_style=ft.TextStyle(size=12, color=MUTED),
            content_padding=ft.padding.symmetric(7, 10),
            **kwargs,
        )

    codigo = input_field("Código", 150)
    titulo = input_field("Título", 340)
    tipo = ft.Dropdown(
        label="Tipo",
        value="Libro",
        width=130,
        bgcolor=SURFACE,
        border_color=BORDER,
        focused_border_color=ACCENT,
        text_size=13,
        label_style=ft.TextStyle(size=12, color=MUTED),
        options=[ft.dropdown.Option("Libro"), ft.dropdown.Option("Revista")],
    )
    autor = input_field("Autor", 240)
    isbn = input_field("ISBN", 170)
    edicion = input_field("Edición", 110, value="1", visible=False)
    precio = input_field("Precio ($)", 150)
    stock = input_field("Stock", 110)
    for campo_ui in [codigo, titulo, autor, isbn, edicion, precio, stock]:
        campo_ui.on_change = lambda e: None

    filtro = input_field("Buscar", 280)
    mensaje = ft.Text(size=12, color=MUTED)
    resumen = ft.Text(size=12, color=MUTED)
    historial = ft.Text(size=11, color=MUTED)

    tabla = ft.DataTable(
        columns=[ft.DataColumn(ft.Text(t, size=13, weight=ft.FontWeight.W_500, color=TEXT)) for t in
                 ["Código", "Producto", "Tipo", "Precio", "Stock", ""]],
        rows=[],
        border=ft.border.all(1, BORDER),
        border_radius=6,
        heading_row_color=CANVAS,
        heading_text_style=ft.TextStyle(color=TEXT, weight=ft.FontWeight.W_500),
        data_row_color={ft.ControlState.HOVERED: "#F3F4F6"},
        divider_thickness=0.5,
        column_spacing=20,
    )

    def avisar(texto, error=False):
        mensaje.value = texto
        mensaje.color = DANGER if error else SUCCESS

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
                ft.DataCell(ft.Text(p.codigo, size=13, color=TEXT, font_family="SFMono-Regular, Consolas, monospace")),
                ft.DataCell(ft.Text(m.titulo, size=13, color=TEXT)),
                ft.DataCell(ft.Text("Libro" if isinstance(m, Libro) else "Revista", size=13, color=MUTED)),
                ft.DataCell(ft.Text(f"${p.precio:.2f}", size=13, color=TEXT)),
                ft.DataCell(ft.Text(str(p.stock), size=13, color=TEXT)),
                ft.DataCell(ft.TextButton("Editar",
                            on_click=lambda e, c=p.codigo: seleccionar(c),
                            style=ft.ButtonStyle(color=ACCENT, text_style=ft.TextStyle(size=13)))),
            ]))
        resumen.value = f"{len(productos)} resultados · {len(catalogo.listar())} totales"
        historial.value = "Historial: " + " · ".join(catalogo.historial[-5:])
        page.update()

    def limpiar(e=None):
        nonlocal seleccionado
        seleccionado = None
        codigo.disabled = False
        for campo_ui in [codigo, titulo, autor, isbn, precio, stock]:
            campo_ui.value = ""
        tipo.value = "Libro"
        edicion.value = "1"
        actualizar.disabled = eliminar.disabled = True
        agregar.disabled = False
        avisar("Complete el formulario para agregar un producto.")
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
        avisar(f"Producto {c} cargado.")
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
            avisar(f"Producto {p.codigo} {'actualizado' if editar else 'agregado'}.")
        except ValueError as error:
            avisar(str(error), True)
        refrescar()

    def borrar(e):
        try:
            c = seleccionado
            catalogo.eliminar(c)
            limpiar()
            avisar(f"Producto {c} eliminado.")
        except ValueError as error:
            avisar(str(error), True)
        refrescar()

    estilo_primario = ft.ButtonStyle(
        bgcolor=ACCENT, color=SURFACE,
        text_style=ft.TextStyle(size=13, weight=ft.FontWeight.W_500),
        padding=ft.padding.symmetric(6, 12),
    )
    estilo_secundario = ft.ButtonStyle(
        bgcolor=SURFACE, color=TEXT,
        side=ft.BorderSide(1, BORDER),
        text_style=ft.TextStyle(size=13, weight=ft.FontWeight.W_500),
        padding=ft.padding.symmetric(6, 12),
    )
    estilo_peligro = ft.ButtonStyle(
        color=DANGER,
        side=ft.BorderSide(1, BORDER),
        text_style=ft.TextStyle(size=13, weight=ft.FontWeight.W_500),
        padding=ft.padding.symmetric(6, 12),
    )

    agregar = ft.ElevatedButton("Agregar", style=estilo_primario, on_click=guardar)
    actualizar = ft.ElevatedButton("Actualizar", style=estilo_primario, disabled=True, on_click=lambda e: guardar(e, True))
    eliminar = ft.OutlinedButton("Eliminar", style=estilo_peligro, disabled=True, on_click=borrar)
    nuevo = ft.TextButton("Limpiar", style=ft.ButtonStyle(color=MUTED, text_style=ft.TextStyle(size=13)), on_click=limpiar)

    tipo.on_change = cambiar_tipo
    filtro.on_change = refrescar
    filtro.on_submit = refrescar

    header = ft.Container(
        content=ft.Row([
            ft.Icon(ft.Icons.LIBRARY_BOOKS, size=20, color=HEADER_TEXT),
            ft.Text("Catálogo", size=15, weight=ft.FontWeight.W_600, color=HEADER_TEXT),
        ], spacing=10, vertical_alignment=ft.CrossAxisAlignment.CENTER),
        bgcolor=HEADER_BG,
        padding=ft.padding.symmetric(12, 24),
    )

    formulario = ft.Container(
        content=ft.Column([
            ft.Text("Nuevo producto", size=13, weight=ft.FontWeight.W_600, color=TEXT),
            ft.Divider(height=1, color=BORDER),
            ft.Row([codigo, titulo, tipo], wrap=True, spacing=10),
            ft.Row([autor, isbn, edicion], wrap=True, spacing=10),
            ft.Row([precio, stock], wrap=True, spacing=10),
            ft.Row([agregar, actualizar, eliminar, nuevo], spacing=8),
            mensaje,
        ], spacing=10),
        bgcolor=SURFACE,
        border=ft.border.all(1, BORDER),
        border_radius=6,
        padding=16,
    )

    toolbar = ft.Row([
        ft.Text("Productos", size=14, weight=ft.FontWeight.W_600, color=TEXT),
        ft.Row([filtro, ft.OutlinedButton("Buscar", style=estilo_secundario, on_click=refrescar)], spacing=8),
    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

    tabla_card = ft.Container(
        content=ft.Column([tabla], scroll=ft.ScrollMode.AUTO, spacing=0),
        bgcolor=SURFACE,
        border=ft.border.all(1, BORDER),
        border_radius=6,
    )

    contenido = ft.Container(
        content=ft.Column([formulario, toolbar, tabla_card, resumen, historial], spacing=14),
        width=1012,
        margin=ft.margin.symmetric(horizontal=24, vertical=20),
    )

    page.add(header, ft.Row([contenido], alignment=ft.MainAxisAlignment.CENTER, expand=True))
    refrescar()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--web", action="store_true")
    parser.add_argument("--port", type=int, default=8550)
    args = parser.parse_args()
    ft.app(target=main, view=ft.AppView.WEB_BROWSER if args.web else ft.AppView.FLET_APP,
           port=args.port if args.web else 0, host="127.0.0.1")
