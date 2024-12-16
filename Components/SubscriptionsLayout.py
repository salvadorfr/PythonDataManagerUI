import flet as ft
import pandas as pd
from datetime import datetime
from Components.colors import *
from functions import read_csv_file, validate_subscription_date, update_csv_file
from typing import Callable, List, Optional

# Pure functions for table operations
calculate_total_pages = lambda df, rows_per_page: len(df) // rows_per_page + (1 if len(df) % rows_per_page > 0 else 0)
get_page_slice = lambda df, page, rows_per_page: df.iloc[(page - 1) * rows_per_page:page * rows_per_page]
format_date = lambda date: datetime.strptime(date, '%Y-%m-%d').strftime('%Y-%m-%d')

# Higher order function for button creation
def create_action_button(icon: str, tooltip: str, action: Callable) -> ft.IconButton:
    return ft.IconButton(
        icon=icon,
        tooltip=tooltip,
        on_click=action,
        icon_color=secondary_color
    )

# Pure function for creating table rows
def create_table_row(row: pd.Series, status: str, action_btn: ft.IconButton) -> ft.DataRow:
    return ft.DataRow(
        cells=[
            ft.DataCell(ft.Text(row['First Name'])),
            ft.DataCell(ft.Text(row['Last Name'])),
            ft.DataCell(ft.Text(str(row['Subscription Date'])[:10])),
            ft.DataCell(ft.Text(status)),
            ft.DataCell(action_btn),
        ]
    )

class SubscriptionsTable(ft.UserControl):
    def __init__(self, mainPage : ft.Page):
        super().__init__()
        self.mPage = mainPage
        self.current_page = 1
        self.rows_per_page = 20
        self.current_df = None
        self.current_status = None  # Add status tracking
        self.setup_controls()
        self.setup_table()
        self.setup_pagination_controls()

    def setup_controls(self):
        self.valid_button = ft.ElevatedButton(
            "Show Valid Subscriptions",
            on_click=self.show_valid_subscriptions,
            bgcolor=ft.Colors.GREEN,
            color = table_bgcolor
        )
        self.invalid_button = ft.ElevatedButton(
            "Show Invalid Subscriptions",
            on_click=self.show_invalid_subscriptions,
            bgcolor=ft.Colors.RED,
            color = table_bgcolor
        )
        self.controls_row = ft.Row([
            self.valid_button, 
            self.invalid_button
        ])

    def setup_table(self):
        self.table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("First Name", width=150)),
                ft.DataColumn(ft.Text("Last Name", width=150)),
                ft.DataColumn(ft.Text("Subscription Date", width=200)),
                ft.DataColumn(ft.Text("Status", width=150)),
                ft.DataColumn(ft.Text("Actions", width=100)),
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
        self.page_info = ft.Text(f"Page {self.current_page}", color=table_txt_color)
        self.pagination = ft.Row(
            controls=[
                ft.IconButton(
                    icon=ft.Icons.ARROW_BACK,
                    on_click=self.prev_page,
                    disabled=True,
                    icon_color=primary_color
                ),
                self.page_info,
                ft.IconButton(
                    icon=ft.Icons.ARROW_FORWARD,
                    on_click=self.next_page,
                    icon_color=primary_color
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )

    def next_page(self, e):
        if self.current_df is not None:
            total_pages = len(self.current_df) // self.rows_per_page + (1 if len(self.current_df) % self.rows_per_page > 0 else 0)
            if self.current_page < total_pages:
                self.current_page += 1
                self.update_table_data(self.current_df, self.current_status)

    def prev_page(self, e):
        if self.current_page > 1:
            self.current_page -= 1
            self.update_table_data(self.current_df, self.current_status)

    def show_valid_subscriptions(self, e):
        try:
            result = validate_subscription_date()
            self.current_page = 1
            self.current_status = "Valid"
            
            if not result['valid'].empty:
                self.update_table_data(result['valid'], self.current_status)
            else:
                self.table.rows.clear()
                self.update()
        except Exception as e:
            print(f"Error in show_valid_subscriptions: {str(e)}")

    def show_invalid_subscriptions(self, e):
        try:
            df = read_csv_file()
            
            current_year = 2024
            # Use correct column name 'Subscription Date' with space
            df['Subscription Date'] = pd.to_datetime(df['Subscription Date'])
            expired_df = df[df['Subscription Date'].dt.year < current_year]
            
            self.current_page = 1
            self.current_status = "Invalid"  # Set status
            if not expired_df.empty:
                self.update_table_data(expired_df, self.current_status)
        except Exception as e:
            print(f"Error in show_invalid_subscriptions: {str(e)}")

    def update_table_data(self, df, status):
        try:
            if df is None or df.empty:
                return
                
            self.current_df = df
            self.table.rows.clear()
            
            total_pages = calculate_total_pages(df, self.rows_per_page)
            page_data = get_page_slice(df, self.current_page, self.rows_per_page)
            
            # Update pagination controls
            self.pagination.controls[0].disabled = self.current_page <= 1
            self.pagination.controls[2].disabled = self.current_page >= total_pages
            self.page_info.value = f"Page {self.current_page} of {total_pages}"
            
            # Create rows using pure functions
            self.table.rows.extend([
                create_table_row(
                    row,
                    status,
                    create_action_button(
                        ft.Icons.UPDATE,
                        "Update Subscription",
                        lambda e, idx=i: self.show_update_dialog_for_row(e, page_data, idx)
                    )
                )
                for i, (_, row) in enumerate(page_data.iterrows())
            ])
            
            self.update()
        except Exception as e:
            print(f"Error updating table: {str(e)}")

    def show_update_dialog_for_row(self, e, df, row_idx):
        alertDialog = ft.AlertDialog(
            actions = [
                ft.TextButton(
                    "Update", style=ft.ButtonStyle(color=ft.Colors.GREEN), on_click= lambda e:self.updateDateMembership(alertDialog, df, row_idx)
                ),
                ft.TextButton(
                    "Cancel", style=ft.ButtonStyle(color=ft.Colors.RED), on_click= lambda e:self.mPage.close(alertDialog)
                )
            ],
            modal = True,
            title = ft.Text("Update membership"),
            content= ft.Text("Are you sure you want to update the membership?"),
            bgcolor=table_bgcolor,
            title_text_style=ft.TextStyle(color=table_txt_color, weight=ft.FontWeight.BOLD, size=20),
            content_text_style=ft.TextStyle(color=table_txt_color)
        )

        self.mPage.open(alertDialog)

    def updateDateMembership(self, dialog, df, idx):
        selected_ID = df.iloc[idx]["Customer Id"]
        fullDf = read_csv_file()
        fullDf.loc[fullDf['Customer Id'] == selected_ID, 'Subscription Date'] = datetime.now().strftime('%Y-%m-%d')
        update_csv_file(fullDf)
        self.mPage.close(dialog)
        self.show_valid_subscriptions
        self.mPage.update()

    def build(self):
        return ft.Container(
            bgcolor=container_color,
            width=1100,
            padding=10,
            border_radius=10,
            content=ft.Column([
                ft.Text(
                    "Subscription Validation",
                    weight=ft.FontWeight.BOLD,
                    size=20,
                    color=table_txt_color
                ),
                self.controls_row,
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
                    height=400,  # Fixed height for vertical scroll
                    width=1050,  # Container width
                    border_radius=10,
                ),
                self.pagination
            ])
        )