import flet as ft
from Components.colors import *

class Header(ft.UserControl):
    def __init__(self):
        super().__init__()

        self.container = ft.Container(
            height=100,
            width=1200,
            bgcolor=primary_color,
            padding=ft.Padding(20,10,20,10),
            content=ft.Text(
                "Company Membership Manager", 
                color="white", 
                size=35, 
                weight=ft.FontWeight.BOLD
            )
        )
    
    def build(self):
        return self.container