import pandas as pd
from django.core.management.base import BaseCommand
from stocks.models import Company, StockData
from tqdm import tqdm
import os
from datetime import datetime

class Command(BaseCommand):
    help = "Import stock data from CSV with comprehensive error handling"

    def handle(self, *args, **options):
        csv_path = os.path.normpath(r"D:\Kareem\Desktop\stock_app\dump.csv")

        if not os.path.exists(csv_path):
            self.stdout.write(self.style.ERROR(f"File not found: {csv_path}"))
            return

        try:
            df = pd.read_csv(
                csv_path,
                na_values=['', 'NA', 'N/A', 'NaN', 'null'],
                keep_default_na=True
            )

            required_columns = {
                'index_name', 'index_date',
                'open_index_value', 'high_index_value',
                'low_index_value', 'closing_index_value', 'volume'
            }
            if not required_columns.issubset(df.columns):
                missing = required_columns - set(df.columns)
                self.stdout.write(self.style.ERROR(f"Missing columns in CSV: {missing}"))
                return

            column_mapping = {
                'index_name': 'ticker',
                'index_date': 'date',
                'open_index_value': 'open',
                'high_index_value': 'high',
                'low_index_value': 'low',
                'closing_index_value': 'close'
            }
            df = df.rename(columns=column_mapping)

            def parse_date(date_str):
                try:
                    return datetime.strptime(str(date_str), '%Y-%m-%d').date()
                except ValueError:
                    try:
                        return datetime.strptime(str(date_str), '%d-%m-%Y').date()
                    except ValueError:
                        return None

            df['date'] = df['date'].apply(parse_date)
            df['volume'] = pd.to_numeric(df['volume'], errors='coerce').fillna(0).astype(int)

            if df['date'].isna().any():
                invalid_count = df['date'].isna().sum()
                self.stdout.write(self.style.WARNING(f"Dropping {invalid_count} rows with invalid dates"))
                df = df.dropna(subset=['date'])

            chunk_size = 1000
            total_rows = len(df)

            with tqdm(total=total_rows, desc="Importing data") as pbar:
                for i in range(0, total_rows, chunk_size):
                    chunk = df.iloc[i:i + chunk_size]

                    for ticker, group in chunk.groupby('ticker'):
                        company, _ = Company.objects.get_or_create(
                            ticker=ticker,
                            defaults={'name': ticker}
                        )

                        # Create list of StockData objects with NaN handling
                        stock_entries = []
                        for _, row in group.iterrows():
                            try:
                                stock_data = StockData(
                                    company=company,
                                    date=row['date'],
                                    open=row['open'],
                                    high=row['high'],
                                    low=row['low'],
                                    close=row['close'],
                                    volume=int(row['volume']) if not pd.isna(row['volume']) else 0
                                )
                                stock_entries.append(stock_data)
                            except Exception as e:
                                self.stdout.write(self.style.WARNING(
                                    f"Skipping row due to error: {str(e)}"
                                ))
                                continue

                        if stock_entries:
                            StockData.objects.bulk_create(stock_entries, ignore_conflicts=True)
                    pbar.update(len(chunk))

            self.stdout.write(self.style.SUCCESS(f"Successfully imported {len(df)} records"))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error during import: {str(e)}"))
            import traceback
            self.stdout.write(self.style.ERROR(f"Traceback: {traceback.format_exc()}"))
