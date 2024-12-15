import flet as ft
from Components.colors import *
from functions import read_csv_file, filter_csv_city, filter_csv_country
from typing import Callable, List, Optional
import pandas as pd

# Pure functions for table operations
calculate_total_pages = lambda df, rows_per_page: len(df) // rows_per_page + (1 if len(df) % rows_per_page > 0 else 0)
get_page_slice = lambda df, page, rows_per_page: df.iloc[(page - 1) * rows_per_page:page * rows_per_page]
create_data_cell = lambda value: ft.DataCell(ft.Text(str(value)))

# Higher order function for creating table rows
def create_table_row(row_data: pd.Series) -> ft.DataRow:
    return ft.DataRow(
        cells=[
            create_data_cell(row_data[col]) for col in 
            ['First Name', 'Last Name', 'Company', 'City', 'Country', 'Email', 'Website']
        ]
    )

# Pure function for pagination state
def get_pagination_state(current_page: int, total_pages: int) -> dict:
    return {
        'prev_disabled': current_page <= 1,
        'next_disabled': current_page >= total_pages,
        'page_info': f"Page {current_page} of {total_pages}"
    }

# Pure function for filtering
def filter_data(df: pd.DataFrame, filter_fn: Callable, value: str) -> pd.DataFrame:
    return filter_fn(value) if value else df

class GeneralTable(ft.UserControl):
    def __init__(self):
        super().__init__()
        # Add pagination state
        self.current_page = 1
        self.rows_per_page = 20
        self.current_df = None
        self.setup_search_controls()
        self.setup_table()
        self.setup_pagination_controls()

    def did_mount(self):
        self.load_initial_data()
        self.update()

    def setup_search_controls(self):
        self.search_input = ft.TextField(
            label="Search by City or Country",
            width=300,
            bgcolor=ft.colors.BLACK,
            border_radius=5
        )
        
        self.search_controls = ft.Row([
            self.search_input,
            ft.ElevatedButton("Search City", on_click=self.filter_by_city),
            ft.ElevatedButton("Search Country", on_click=self.filter_by_country),
            ft.ElevatedButton("Show All", on_click=self.show_all_data)
        ])

    def setup_table(self):
        self.table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("First Name", width=150)),
                ft.DataColumn(ft.Text("Last Name", width=150)),
                ft.DataColumn(ft.Text("Company", width=200)),
                ft.DataColumn(ft.Text("City", width=150)),
                ft.DataColumn(ft.Text("Country", width=150)),
                ft.DataColumn(ft.Text("Email", width=200)),
                ft.DataColumn(ft.Text("Website", width=200)),
            ],
            rows=[],
            heading_text_style=ft.TextStyle(
                color=table_txt_color,
                weight=ft.FontWeight.BOLD
            ),
            data_text_style=ft.TextStyle(
                color=table_txt_color,            
            ),
            bgcolor=table_bgcolor,
            border_radius=10,
        )

    def setup_pagination_controls(self):
        self.page_info = ft.Text(f"Page {self.current_page}")
        self.pagination = ft.Row(
            controls=[
                ft.IconButton(
                    icon=ft.icons.ARROW_BACK,
                    on_click=self.prev_page,
                    disabled=True
                ),
                self.page_info,
                ft.IconButton(
                    icon=ft.icons.ARROW_FORWARD,
                    on_click=self.next_page
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )

    def load_initial_data(self):
        df = read_csv_file()
        self.update_table_data(df)

    def update_table_data(self, df):
        if df is None or df.empty:
            print("Debug - No data to display")
            return
            
        self.current_df = df
        self.table.rows.clear()
        
        total_pages = calculate_total_pages(df, self.rows_per_page)
        page_data = get_page_slice(df, self.current_page, self.rows_per_page)
        pagination_state = get_pagination_state(self.current_page, total_pages)
        
        # Update pagination controls
        self.pagination.controls[0].disabled = pagination_state['prev_disabled']
        self.pagination.controls[2].disabled = pagination_state['next_disabled']
        self.page_info.value = pagination_state['page_info']
        
        # Update table rows using pure function
        self.table.rows.extend([create_table_row(row) for _, row in page_data.iterrows()])
        self.update()

    def filter_by_city(self, e):
        if self.search_input.value:
            filtered_df = filter_data(self.current_df, filter_csv_city, self.search_input.value)
            print(f"Debug - Filtered rows: {len(filtered_df)}")  # Debug print
            self.current_page = 1  # Reset to first page
            if not filtered_df.empty:
                self.update_table_data(filtered_df)
            else:
                # Clear table if no results
                self.table.rows.clear()
                self.update()

    def filter_by_country(self, e):
        if self.search_input.value:
            filtered_df = filter_data(self.current_df, filter_csv_country, self.search_input.value)
            print(f"Debug - Filtered rows: {len(filtered_df)}")  # Debug print
            self.current_page = 1  # Reset to first page
            if not filtered_df.empty:
                self.update_table_data(filtered_df)
            else:
                # Clear table if no results
                self.table.rows.clear()
                self.update()

    def show_all_data(self, e):
        self.search_input.value = ""
        self.load_initial_data()
        self.update()

    def next_page(self, e):
        if self.current_df is not None:
            total_pages = len(self.current_df) // self.rows_per_page + (1 if len(self.current_df) % self.rows_per_page > 0 else 0)
            if self.current_page < total_pages:
                self.current_page += 1
                self.update_table_data(self.current_df)

    def prev_page(self, e):
        if self.current_page > 1:
            self.current_page -= 1
            self.update_table_data(self.current_df)

    def build(self):
        return ft.Container(
            bgcolor=container_color,
            width=1100,
            padding=10,
            border_radius=10,
            content=ft.Column([
                ft.Text(
                    "Members Information",
                    weight=ft.FontWeight.BOLD,
                    size=20,
                    color=table_txt_color
                ),
                self.search_controls,
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Row(
                                [self.table],
                                scroll="always",
                                width=1400
                            )
                        ],
                        scroll="always",
                    ),
                    height=400,
                    width=1050,
                    border_radius=10,
                ),
                self.pagination
            ])
        )