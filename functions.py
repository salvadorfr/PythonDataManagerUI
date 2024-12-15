import flet as ft
import pandas as pd
import matplotlib as plt
from datetime import datetime
from typing import Dict, Optional, Callable

# Pure functions
def read_csv_file() -> pd.DataFrame:
    try:
        df = pd.read_csv('customers-10000.csv')
        if df.empty:
            raise ValueError("CSV file is empty")
        return df
    except FileNotFoundError:
        raise FileNotFoundError("CSV file not found")
    except Exception as e:
        raise Exception(f"Error reading CSV: {str(e)}")

# Higher order function for filtering
def create_filter(column: str) -> Callable[[pd.DataFrame, str], pd.DataFrame]:
    def filter_data(df: pd.DataFrame, value: str) -> pd.DataFrame:
        return df[df[column].str.contains(value, case=False, na=False)]
    return filter_data

# Lambda functions for common operations
get_total_rows = lambda df: len(df)
is_empty = lambda df: df.empty
has_column = lambda df, col: col in df.columns
to_datetime = lambda df, col: pd.to_datetime(df[col])
create_mask = lambda df, first, last: (df['First Name'] == first) & (df['Last Name'] == last)

# Filter functions using higher order function
filter_by_city = create_filter('City')
filter_by_country = create_filter('Country')

def filter_csv_city(city: str) -> pd.DataFrame:
    try:
        df = read_csv_file()
        if not has_column(df, 'City'):
            raise KeyError("City column not found")
            
        filtered_rows = filter_by_city(df, city)
        total_rows = get_total_rows(filtered_rows)
        
        if not is_empty(filtered_rows):
            print(f"Records found for city {city}: {total_rows}")
            return filtered_rows
        return pd.DataFrame()
            
    except Exception as e:
        print(f"Error filtering by city: {str(e)}")
        return pd.DataFrame()

def filter_csv_country(country: str) -> pd.DataFrame:
    try:
        df = read_csv_file()
        if not has_column(df, 'Country'):
            raise KeyError("Country column not found")
            
        filtered_rows = filter_by_country(df, country)
        total_rows = get_total_rows(filtered_rows)
        
        if not is_empty(filtered_rows):
            print(f"\nRecords found for country {country}: {total_rows}")
            return filtered_rows
        return pd.DataFrame()
            
    except Exception as e:
        print(f"Error filtering by country: {str(e)}")
        return pd.DataFrame()

# Pure function for subscription validation
def filter_by_year(df: pd.DataFrame, year: int, date_column: str) -> Dict[str, pd.DataFrame]:
    df[date_column] = to_datetime(df, date_column)
    return {
        'valid': df[df[date_column].dt.year >= year],
        'expired': df[df[date_column].dt.year < year]
    }

def validate_subscription_date() -> Dict[str, pd.DataFrame]:
    try:
        df = read_csv_file()
        current_year = 2024
        
        if not has_column(df, 'Subscription Date'):
            raise KeyError("Subscription Date column not found")
        
        result = filter_by_year(df, current_year, 'Subscription Date')
        
        print(f"\nExpired subscriptions found: {get_total_rows(result['expired'])}")
        print(f"Valid subscriptions found: {get_total_rows(result['valid'])}")
        
        return result
        
    except Exception as e:
        print(f"Error in validate_subscription_date: {str(e)}")
        return {
            'valid': pd.DataFrame(),
            'expired': pd.DataFrame()
        }

# Pure function for updating subscription
def update_subscription(df: pd.DataFrame, first_name: str, last_name: str, new_date: str) -> pd.DataFrame:
    mask = create_mask(df, first_name, last_name)
    df.loc[mask, 'Subscription Date'] = new_date
    return df

def update_csv_subscription_date(first_name: str, last_name: str, new_date: str) -> bool:
    try:
        df = read_csv_file()
        print(f"\nUpdating subscription for: {first_name} {last_name}")
        print(f"New date: {new_date}")
        
        mask = create_mask(df, first_name, last_name)
        rows_affected = mask.sum()
        
        if rows_affected == 0:
            print("No matching records found")
            return False
            
        updated_df = update_subscription(df, first_name, last_name, new_date)
        updated_df.to_csv('customers-10000.csv', index=False)
        
        print(f"Updated {rows_affected} record(s)")
        print("CSV file updated successfully")
        
        # Verify update
        verify_df = read_csv_file()
        verify_mask = create_mask(verify_df, first_name, last_name)
        print(f"Verification - New date in CSV: {verify_df.loc[verify_mask, 'Subscription Date'].iloc[0]}")
        
        return True
        
    except Exception as e:
        print(f"Error updating CSV: {str(e)}")
        return False