import flet as ft
from Components.NavBar              import NavBar
from Components.colors              import *
from Components.Header              import Header
from Components.GeneralLayout       import GeneralTable
from Components.SubscriptionsLayout import SubscriptionsTable
from Components.ReportsLayout       import ReportsLayout

def main(page: ft.Page):
    # Function that changes content
    def contentChange(index):
        right_container.content = containersList[index]
        page.update()

    page.fonts = { "Plus Jakarta Sans" : "PlusJakartaSans.ttf" }
    page.theme = ft.Theme( font_family ="Plus Jakarta Sans" )
    page.title              = "Proyect"
    page.window.icon        = "ITLIcon.ico"
    page.window.width       = 1200
    page.window.height      = 700
    page.padding            = 0
    page.bgcolor            = app_bgcolor
    page.window.resizable   = False
    page.vertical_alignment = ft.MainAxisAlignment.START

    # Initialize components
    general = GeneralTable()
    subscriptions = SubscriptionsTable()
    reports = ReportsLayout()
    
    # Create container first
    right_container = ft.Container(
        expand=True,
        height=600,
        padding=ft.Padding(10,10,10,50),
    )
    
    # Create list after container
    containersList = [general, subscriptions, reports]
    
    # Set initial content
    right_container.content = containersList[0]

    header = Header()
    navbar = NavBar(funcContChange=contentChange)
    
    page.add(
        ft.Column(
            controls=[
                header,
                ft.Row(
                    controls=[ navbar, right_container ],
                    expand=True,
                    spacing=0
                )
            ],
            spacing=0
        )
    )

ft.app(target = main)
