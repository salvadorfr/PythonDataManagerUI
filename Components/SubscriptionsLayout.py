import flet as ft
from Components.colors import *

class SubscriptionsTable(ft.UserControl):
    table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Name")),
            ft.DataColumn(ft.Text("Last Name")),
            ft.DataColumn(ft.Text("Phone")),
            ft.DataColumn(ft.Text("Email")),
            ft.DataColumn(ft.Text("Date")),
            ft.DataColumn(ft.Text("Update")),
        ],
        rows=[
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text("Heather")),
                    ft.DataCell(ft.Text("Callahan")),
                    ft.DataCell(ft.Text("043-797-5229")),
                    ft.DataCell(ft.Text("urangel@espinoza-francis.net")),
                    ft.DataCell(ft.Text("26/08/2020")),
                    ft.DataCell(ft.Button("Update",bgcolor="green", color=table_bgcolor))
                ]
            ),
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text("Kristina")),
                    ft.DataCell(ft.Text("Ferrell")),
                    ft.DataCell(ft.Text("932-062-1802")),
                    ft.DataCell(ft.Text("xreese@hall-donovan.com")),
                    ft.DataCell(ft.Text("27/04/2020")),
                    ft.DataCell(ft.Button("Valid",bgcolor=table_bgcolor, color=table_txt_color, disabled=True))
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
        expand=True
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
                        "Subscriptions Table",
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