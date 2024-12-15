import flet as ft
import pandas as pd
from datetime import datetime
from Components.colors import *
from functions import read_csv_file, validate_subscription_date, update_csv_subscription_date

class SubscriptionsTable(ft.UserControl):
    def __init__(self):
        super().__init__()
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
            bgcolor=ft.colors.GREEN
        )
        self.invalid_button = ft.ElevatedButton(
            "Show Invalid Subscriptions",
            on_click=self.show_invalid_subscriptions,
            bgcolor=ft.colors.RED
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
                print(f"Debug: Found {len(result['valid'])} valid subscriptions")
                self.update_table_data(result['valid'], self.current_status)
            else:
                print("Debug: No valid subscriptions found")
                self.table.rows.clear()
                self.update()
        except Exception as e:
            print(f"Error in show_valid_subscriptions: {str(e)}")

    def show_invalid_subscriptions(self, e):
        try:
            df = read_csv_file()
            # Debug print to check column names
            print("Available columns:", df.columns.tolist())
            
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
                print("Debug: No data to update table")
                return
                
            print(f"Debug: Updating table with {len(df)} rows")
            self.current_df = df
            self.table.rows.clear()
            
            # Calculate pagination
            total_pages = len(df) // self.rows_per_page + (1 if len(df) % self.rows_per_page > 0 else 0)
            print(f"Debug: Total pages: {total_pages}")
            
            # Update navigation buttons state
            self.pagination.controls[0].disabled = self.current_page <= 1
            self.pagination.controls[2].disabled = self.current_page >= total_pages
            
            # Update page info
            self.page_info.value = f"Page {self.current_page} of {total_pages}"
            
            # Calculate page slices
            start_idx = (self.current_page - 1) * self.rows_per_page
            end_idx = start_idx + self.rows_per_page
            page_data = df.iloc[start_idx:end_idx]
            
            for idx, row in page_data.iterrows():
                update_btn = ft.IconButton(
                    icon=ft.icons.UPDATE,
                    tooltip="Update Subscription",
                    on_click=lambda e, row_idx=idx: self.show_update_dialog_for_row(e, row_idx)
                )
                
                self.table.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(row['First Name'])),
                            ft.DataCell(ft.Text(row['Last Name'])),
                            ft.DataCell(ft.Text(str(row['Subscription Date']))),
                            ft.DataCell(ft.Text(status)),
                            ft.DataCell(update_btn),
                        ]
                    )
                )
            self.update()
        except Exception as e:
            print(f"Error updating table: {str(e)}")

    def show_update_dialog_for_row(self, e, row_idx):
        def close_dlg(e):
            self.update_dialog.open = False
            self.page.update()  # Update page reference

        def update_subscription(e):
            try:
                date_value = self.page.get_value(self.date_picker)  # Get selected date
                if date_value:
                    current_row = self.current_df.iloc[row_idx]
                    formatted_date = datetime.strptime(date_value, '%Y-%m-%d').strftime('%Y-%m-%d')
                    
                    success = update_csv_subscription_date(
                        current_row['First Name'],
                        current_row['Last Name'],
                        formatted_date
                    )
                    
                    if success:
                        mask = (self.current_df['First Name'] == current_row['First Name']) & \
                              (self.current_df['Last Name'] == current_row['Last Name'])
                        self.current_df.loc[mask, 'Subscription Date'] = formatted_date
                        print("Update successful")
                        self.update_table_data(self.current_df, self.current_status)
                        close_dlg(e)
                    else:
                        print("Failed to update subscription")
            except Exception as e:
                print(f"Error updating subscription: {str(e)}")

        self.date_picker = ft.DatePicker(
            first_date=datetime(2024, 1, 1),
            last_date=datetime(2024, 12, 31),
            on_change=lambda e: print(f"Selected date: {e.control.value}")  # Debug selected date
        )
        self.page.overlay.append(self.date_picker)  # Add picker to page overlay
        
        self.update_dialog = ft.AlertDialog(
            title=ft.Text("Update Subscription Date"),
            content=ft.Column([
                ft.Text("Select new subscription date:"),
                ft.ElevatedButton(
                    "Pick Date",
                    icon=ft.icons.CALENDAR_TODAY,
                    on_click=lambda _: self.date_picker.pick_date()
                )
            ]),
            actions=[
                ft.TextButton("Update", on_click=update_subscription),
                ft.TextButton("Cancel", on_click=close_dlg),
            ],
        )
        
        self.update_dialog.open = True
        self.page.update()

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