# Bookstore Inventory and Analytics System

## Project Objective
A Python-based bookstore management and analytics project covering inventory management, sales recording, data cleaning, NumPy/Pandas analysis, OOP and visualization.

## Files
- `bookstore_system.py` — main OOP application
- `bookstore_analysis.ipynb` — Jupyter Notebook with analysis and visualizations
- `inventory.csv` — inventory dataset
- `sales.csv` — sales dataset
- `README.md` — setup and project documentation

## Technologies
Python, NumPy, Pandas, Matplotlib, Seaborn, Jupyter Notebook.

## Installation
```bash
pip install numpy pandas matplotlib seaborn jupyter
```

## Run the Python application
```bash
python bookstore_system.py
```

## Open the notebook
```bash
jupyter notebook bookstore_analysis.ipynb
```

## Main OOP Methods
- `add_book(title, author, genre, price, quantity)`
- `update_inventory(title, quantity)`
- `remove_book(title)`
- `record_sale(title, quantity)`
- `generate_report()`

## Visualizations
The notebook produces:
1. Monthly revenue line chart
2. Sales by genre bar chart
3. Top 10 books bar chart
4. Revenue share by genre pie chart
5. Price vs sales volume scatter plot
6. Price/sales/revenue correlation heatmap
7. Inventory stock-status chart

## Suggested student workflow
Load -> Inspect -> Clean -> Validate -> Analyze -> Visualize -> Report.
