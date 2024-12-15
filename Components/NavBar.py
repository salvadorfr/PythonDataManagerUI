import flet as ft
from Components.colors import *

class NavBar(ft.UserControl):
    def __init__(self, funcContChange):
        super().__init__()

        self.funcContChange = funcContChange

        self.container = ft.Container(
            width=100,
            height=600,
            bgcolor=primary_color,

            content=ft.Column(
                controls=[
                    ft.Container(
                        expand = True,
                        content=ft.NavigationRail(
                            destinations=[
                                ft.NavigationRailDestination(
                                    icon            = ft.Icons.HOME_OUTLINED,
                                    selected_icon   = ft.Icons.HOME
                                ),
                                ft.NavigationRailDestination(
                                    icon            = ft.Icons.PERSON_OUTLINED,
                                    selected_icon   = ft.Icons.PERSON
                                ),
                                ft.NavigationRailDestination(
                                    icon            = ft.Icons.ARTICLE_OUTLINED,
                                    selected_icon   = ft.Icons.ARTICLE
                                )
                            ],
                            expand=True,
                            selected_index=0,
                            bgcolor=secondary_color,
                            indicator_color=primary_color,
                            on_change = self.optionChange
                        )
                    )
                ]
            )
        )

    def optionChange(self, e):
        self.funcContChange(e.control.selected_index)

    def build(self):
        return self.container
