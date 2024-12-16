import flet as ft
from Components.NavBar import NavBar
from Components.colors import *
from Components.Header import Header
from Components.GeneralLayout import GeneralTable
from Components.SubscriptionsLayout import SubscriptionsTable
from Components.ReportsLayout import ReportsLayout
from typing import List, Callable

# Pure functions for UI operations
create_window_config = lambda: {
    "title": "Proyect",
    "icon": "ITLIcon.ico",
    "width": 1200,
    "height": 700,
    "resizable": False
}

create_page_config = lambda bgcolor: {
    "padding": 0,
    "bgcolor": bgcolor,
    "vertical_alignment": ft.MainAxisAlignment.START,
    "fonts": {"Plus Jakarta Sans": "PlusJakartaSans.ttf"}
}

# Higher order function for container creation
def create_container(content=None):
    return ft.Container(
        expand=True,
        height=600,
        padding=ft.Padding(10,10,10,0),
        content=content
    )

# Pure function for layout composition
def create_layout(header: ft.Control, navbar: ft.Control, container: ft.Control) -> ft.Column:
    return ft.Column(
        controls=[
            header,
            ft.Row(
                controls=[navbar, container],
                expand=True,
                spacing=0
            )
        ],
        spacing=0
    )

def main(page: ft.Page):
    # Apply configurations using pure functions
    window_config = create_window_config()
    page_config = create_page_config(app_bgcolor)
    
    # Apply window configuration
    for key, value in window_config.items():
        setattr(page.window, key, value)
    
    # Apply page configuration
    for key, value in page_config.items():
        setattr(page, key, value)

    # Initialize components with functional approach
    components = {
        'general': GeneralTable(),
        'subscriptions': SubscriptionsTable(page),
        'reports': ReportsLayout()
    }
    
    # Create container with functional approach
    right_container = create_container()
    containersList = [components['general'], components['subscriptions'], components['reports']]
    
    # Pure function for content change
    contentChange = lambda index: setattr(right_container, 'content', containersList[index])
    
    # Set initial content
    right_container.content = containersList[0]

    # Create layout with pure function
    layout = create_layout(
        Header(),
        NavBar(funcContChange=lambda i: [contentChange(i), page.update()]),
        right_container
    )
    
    page.add(layout)

ft.app(target=main)
