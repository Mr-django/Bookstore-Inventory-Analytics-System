"""
Bookstore Inventory and Analytics System
Run:
    python bookstore_system.py
"""

from pathlib import Path
from datetime import datetime
import numpy as np
import pandas as pd


class Bookstore:
    """Manage bookstore inventory and sales data."""

    def __init__(self, inventory_file="inventory.csv", sales_file="sales.csv"):
        self.inventory_file = Path(inventory_file)
        self.sales_file = Path(sales_file)
        self.inventory = self._load_inventory()
        self.sales = self._load_sales()

    def _load_inventory(self):
        if not self.inventory_file.exists():
            return pd.DataFrame(
                columns=["Book_ID", "Title", "Author", "Genre", "Price", "Quantity"]
            )
        df = pd.read_csv(self.inventory_file)
        df["Price"] = pd.to_numeric(df["Price"], errors="coerce")
        df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")
        return df

    def _load_sales(self):
        if not self.sales_file.exists():
            return pd.DataFrame(
                columns=[
                    "Sale_ID", "Date", "Book_ID", "Title", "Author", "Genre",
                    "Unit_Price", "Quantity", "Revenue"
                ]
            )
        df = pd.read_csv(self.sales_file)
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")
        df["Unit_Price"] = pd.to_numeric(df["Unit_Price"], errors="coerce")
        df["Revenue"] = pd.to_numeric(df["Revenue"], errors="coerce")
        return df

    def save_data(self):
        self.inventory.to_csv(self.inventory_file, index=False)
        self.sales.to_csv(self.sales_file, index=False)

    def add_book(self, title, author, genre, price, quantity):
        """Add a new book after validating inputs."""
        if not title.strip():
            raise ValueError("Title cannot be empty.")
        if price <= 0:
            raise ValueError("Book price must be positive.")
        if quantity < 0:
            raise ValueError("Quantity cannot be negative.")
        if title.lower() in self.inventory["Title"].astype(str).str.lower().values:
            raise ValueError("Book already exists.")

        next_id = len(self.inventory) + 1
        book_id = f"B{next_id:03d}"
        new_row = pd.DataFrame([{
            "Book_ID": book_id,
            "Title": title,
            "Author": author,
            "Genre": genre,
            "Price": price,
            "Quantity": quantity
        }])
        self.inventory = pd.concat([self.inventory, new_row], ignore_index=True)
        return book_id

    def update_inventory(self, title, quantity):
        """Update stock quantity for an existing book."""
        if quantity < 0:
            raise ValueError("Quantity cannot be negative.")
        mask = self.inventory["Title"].str.lower() == title.lower()
        if not mask.any():
            raise ValueError("Book not found.")
        self.inventory.loc[mask, "Quantity"] = quantity

    def remove_book(self, title):
        """Remove a book from inventory."""
        mask = self.inventory["Title"].str.lower() == title.lower()
        if not mask.any():
            raise ValueError("Book not found.")
        self.inventory = self.inventory.loc[~mask].reset_index(drop=True)

    def record_sale(self, title, quantity):
        """Deduct sold books from inventory and append a sale record."""
        if quantity <= 0:
            raise ValueError("Sale quantity must be positive.")

        mask = self.inventory["Title"].str.lower() == title.lower()
        if not mask.any():
            raise ValueError("Book not found.")

        book = self.inventory.loc[mask].iloc[0]
        if book["Quantity"] < quantity:
            raise ValueError(
                f"Insufficient stock. Available quantity: {int(book['Quantity'])}"
            )

        self.inventory.loc[mask, "Quantity"] -= quantity

        sale_no = len(self.sales) + 1
        revenue = float(book["Price"] * quantity)
        new_sale = pd.DataFrame([{
            "Sale_ID": f"S{sale_no:04d}",
            "Date": datetime.now().strftime("%Y-%m-%d"),
            "Book_ID": book["Book_ID"],
            "Title": book["Title"],
            "Author": book["Author"],
            "Genre": book["Genre"],
            "Unit_Price": book["Price"],
            "Quantity": quantity,
            "Revenue": revenue
        }])

        self.sales = pd.concat([self.sales, new_sale], ignore_index=True)
        return revenue

    def generate_report(self):
        """Summarize inventory and sales metrics using Pandas and NumPy."""
        revenue = self.sales["Revenue"].fillna(0).to_numpy(dtype=float)
        quantity = self.sales["Quantity"].fillna(0).to_numpy(dtype=float)

        total_revenue = np.sum(revenue)
        total_units = np.sum(quantity)
        average_price = np.mean(
            self.inventory["Price"].dropna().to_numpy(dtype=float)
        )
        low_stock = int((self.inventory["Quantity"] <= 5).sum())

        print("\n========== BOOKSTORE REPORT ==========")
        print(f"Books in inventory : {len(self.inventory)}")
        print(f"Total units sold   : {int(total_units)}")
        print(f"Total revenue      : ₹{total_revenue:,.2f}")
        print(f"Average book price : ₹{average_price:,.2f}")
        print(f"Low-stock books    : {low_stock}")

        if not self.sales.empty:
            top_books = (
                self.sales.groupby("Title")["Quantity"]
                .sum()
                .sort_values(ascending=False)
                .head(5)
            )
            print("\nTop 5 selling books:")
            print(top_books.to_string())

        return {
            "books_in_inventory": len(self.inventory),
            "total_units_sold": int(total_units),
            "total_revenue": float(total_revenue),
            "average_book_price": float(average_price),
            "low_stock_books": low_stock,
        }


def main():
    store = Bookstore()
    store.generate_report()

    print("\nSample inventory:")
    print(store.inventory.head())

    print("\nSample sales:")
    print(store.sales.head())


if __name__ == "__main__":
    main()
