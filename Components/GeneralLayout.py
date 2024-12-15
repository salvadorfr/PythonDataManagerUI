import flet as ft
from Components.colors import *

class GeneralTable(ft.UserControl):
    table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Id")),
            ft.DataColumn(ft.Text("Name")),
            ft.DataColumn(ft.Text("Last Name")),
            ft.DataColumn(ft.Text("Company")),
            ft.DataColumn(ft.Text("City")),
            ft.DataColumn(ft.Text("Website")),
        ],
        rows=[
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text("1")),
                    ft.DataCell(ft.Text("Heather")),
                    ft.DataCell(ft.Text("Callahan")),
                    ft.DataCell(ft.Text("Mosley-David")),
                    ft.DataCell(ft.Text("Lake Jeffboro")),
                    ft.DataCell(ft.Text("http://www.escobar.org/"))
                ]
            ),
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text("2")),
                    ft.DataCell(ft.Text("Kristina")),
                    ft.DataCell(ft.Text("Ferrell")),
                    ft.DataCell(ft.Text("Horn, Shepard")),
                    ft.DataCell(ft.Text("Aaronville")),
                    ft.DataCell(ft.Text("http://tyler-pugh.info/"))
                ]
            )
        ],
        heading_text_style=ft.TextStyle(
            color=table_txt_color,
            weight=ft.FontWeight.BOLD
        ),
        data_text_style=ft.TextStyle(
            color=table_txt_color,            
        ),
        bgcolor = table_bgcolor,
        border_radius= 10,
        expand = True,
    )

    def __init__(self):
        super().__init__()

        self.container = ft.Container(
            bgcolor = container_color,
            width=1100,
            padding=10,
            border_radius= 10,
            content = ft.Column(
                controls=[
                    ft.Text(
                        "Members Information",
                        weight = ft.FontWeight.BOLD,
                        size =20,
                        color = table_txt_color
                    ),
                    self.table
                ]
            )
        )

    def build(self):
        return self.container