import flet as ft
import pandas as pd
import matplotlib as plt
from datetime import datetime

def read_csv_file():
    try:
        df = pd.read_csv('customers-10000.csv')
        if df.empty:
            raise ValueError("CSV file is empty")
        return df
    except FileNotFoundError:
        raise FileNotFoundError("CSV file not found")
    except Exception as e:
        raise Exception(f"Error reading CSV: {str(e)}")

def filter_csv_city(city: str):
    try:
        df = read_csv_file()
        if 'City' not in df.columns:
            raise KeyError("City column not found")
            
        filtered_rows = df[df['City'].str.contains(city, case=False, na=False)]
        total_rows = len(filtered_rows)
        
        if not filtered_rows.empty:
            print(f"Records found for city {city}: {total_rows}")
            return filtered_rows
        return pd.DataFrame()
            
    except Exception as e:
        print(f"Error filtering by city: {str(e)}")
        return pd.DataFrame()

def filter_csv_country(country: str):
    try:
        df = read_csv_file()
        if 'Country' not in df.columns:
            raise KeyError("Country column not found")
            
        filtered_rows = df[df['Country'].str.contains(country, case=False, na=False)]
        total_rows = len(filtered_rows)
        
        if not filtered_rows.empty:
            print(f"\nRecords found for country {country}: {total_rows}")
            return filtered_rows
        return pd.DataFrame()
            
    except Exception as e:
        print(f"Error filtering by country: {str(e)}")
        return pd.DataFrame()
    
def validate_subscription_date():
    try:
        df = read_csv_file()
        current_year = 2024
        
        print("\nDebug - Columns in DataFrame:", df.columns.tolist())
        
        if 'Subscription Date' not in df.columns:
            raise KeyError("Subscription Date column not found")
        
        # Convert and validate dates
        df['Subscription Date'] = pd.to_datetime(df['Subscription Date'])
        print("Debug - Date conversion successful")
        
        # Filter subscriptions
        expired_subscriptions = df[df['Subscription Date'].dt.year < current_year]
        valid_subscriptions = df[df['Subscription Date'].dt.year >= current_year]
        
        print(f"\nExpired subscriptions found: {len(expired_subscriptions)}")
        print(f"Valid subscriptions found: {len(valid_subscriptions)}")
        
        if expired_subscriptions.empty and valid_subscriptions.empty:
            print("Debug - No subscriptions found after filtering")
            
        return {
            'valid': valid_subscriptions,
            'expired': expired_subscriptions
        }
        
    except Exception as e:
        print(f"Error in validate_subscription_date: {str(e)}")
        return {
            'valid': pd.DataFrame(),
            'expired': pd.DataFrame()
        }

def update_csv_subscription_date(first_name, last_name, new_date):
    try:
        df = read_csv_file()
        print(f"\nUpdating subscription for: {first_name} {last_name}")
        print(f"New date: {new_date}")
        
        # Find and update matching rows
        mask = (df['First Name'] == first_name) & (df['Last Name'] == last_name)
        rows_affected = mask.sum()
        
        if rows_affected == 0:
            print("No matching records found")
            return False
            
        # Update DataFrame and save
        df.loc[mask, 'Subscription Date'] = new_date
        df.to_csv('customers-10000.csv', index=False)
        
        print(f"Updated {rows_affected} record(s)")
        print("CSV file updated successfully")
        
        # Verify update
        updated_df = read_csv_file()
        verify_mask = (updated_df['First Name'] == first_name) & \
                     (updated_df['Last Name'] == last_name)
        print(f"Verification - New date in CSV: {updated_df.loc[verify_mask, 'Subscription Date'].iloc[0]}")
        
        return True
        
    except Exception as e:
        print(f"Error updating CSV: {str(e)}")
        return False
