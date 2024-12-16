import flet as ft
from Components.colors import *
import matplotlib.pyplot as plt
import pandas as pd
import io
import base64
from functions import read_csv_file
from typing import Callable, Any
from functools import reduce

# Pure Functions
create_chart_config = lambda title, colors=None: {
    'figsize': (8, 8),
    'kind': 'pie',
    'autopct': '%1.1f%%',
    'colors': colors,
    'title': title
}

process_subscription = lambda df: (
    df['Subscription Date']
    .pipe(pd.to_datetime)
    .apply(lambda x: 'Valid' if x.year >= 2024 else 'Invalid')
    .value_counts()
)

process_cities = lambda df, country: (
    df[df['Country'] == country]['City'].value_counts()
)

# Higher Order Functions
def chart_generator(config: dict) -> Callable[[pd.Series], Any]:
    def create(data: pd.Series) -> Any:
        plt.figure(figsize=config['figsize'])
        data.plot(
            kind=config['kind'],
            autopct=config['autopct'],
            colors=config['colors']
        )
        plt.title(config['title'])
        return plt
    return create

def image_processor(plt_instance: Any) -> str:
    buf = io.BytesIO()
    plt_instance.savefig(buf, format='PNG')
    buf.seek(0)
    img_str = base64.b64encode(buf.getvalue()).decode()
    plt_instance.close()
    return img_str

class ReportsLayout(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.setup_ui_components()

    def setup_ui_components(self):
        self.country_input = ft.TextField(
            label="Enter Country Name",
            width=200,
            bgcolor = table_bgcolor,
            border_color=primary_color,
            text_style=ft.TextStyle(color=ft.colors.BLACK)
        )
        
        self.chart_image = ft.Image(
            width=600,
            height=600,
            fit=ft.ImageFit.CONTAIN,
            visible=False,
        )
        
        self.subscription_btn = ft.ElevatedButton(
            text="Generate Subscription Status",
            on_click=self.generate_subscription_chart,
            style=ft.ButtonStyle(
                bgcolor=primary_color,
                color=ft.Colors.WHITE,
            )
        )

        self.cities_btn = ft.ElevatedButton(
            text="Show Cities Distribution",
            on_click=self.generate_cities_chart,
            style=ft.ButtonStyle(
                bgcolor=primary_color,
                color=ft.Colors.WHITE,
            )
        )

        self.menuContainer = ft.Container(
            content=ft.Column(
                [
                    ft.Container(
                        content= ft.Column([ft.Text("Subscription report", style=ft.TextStyle(color=table_txt_color, weight=ft.FontWeight.BOLD)),self.subscription_btn]),
                        bgcolor= container_color,
                        padding=10,
                        border_radius=10
                    ),
                    ft.Container(
                        content= ft.Column([ft.Text("Cities report", style=ft.TextStyle(color=table_txt_color, weight=ft.FontWeight.BOLD)),self.country_input, self.cities_btn]),
                        bgcolor = container_color,
                        padding=10,
                        border_radius=10
                    )
                ]
            )
        )

        self.graphicContainer = ft.Container(
            content = self.chart_image,
            bgcolor= container_color,
            padding= 10,
            width= 600,
            height= 600,
            border_radius = 10
        )

        self.container = ft.Container(
            content= ft.Row(
                [
                    self.menuContainer,
                    self.graphicContainer
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER
            ),
        )

    async def generate_subscription_chart(self, _):
        config = create_chart_config(
            'Subscription Status Distribution',
            ['#2ecc71', '#e74c3c']
        )
        
        chart_pipeline = lambda df: image_processor(
            chart_generator(config)(process_subscription(df))
        )
        
        self.chart_image.src_base64 = chart_pipeline(read_csv_file())
        self.chart_image.visible = True
        await self.update_async()

    async def generate_cities_chart(self, _):
        country = self.country_input.value
        df = read_csv_file()
        
        if country not in df['Country'].values:
            self.chart_image.visible = False
            await self.update_async()
            return
        
        config = create_chart_config(f'City Distribution in {country}')
        chart_pipeline = lambda df: image_processor(
            chart_generator(config)(process_cities(df, country))
        )
        
        self.chart_image.src_base64 = chart_pipeline(df)
        self.chart_image.visible = True
        await self.update_async()

    def build(self):
        return self.container