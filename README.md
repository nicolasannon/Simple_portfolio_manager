# Simple_portfolio_manager
Simple portfolio manager, to create track and / import / export portfolio of stocks / crypto


# Portfolio Manager

A Python-based portfolio management tool that allows you to track and manage different types of financial assets—stocks, bonds, and cryptocurrencies. The application retrieves market data in real-time using [yfinance](https://pypi.org/project/yfinance/) and the Binance API, calculates asset valuations and portfolio PnL, and provides a graphical user interface (GUI) built with Tkinter.

## Features

- **Asset Management:**  
  - Add assets such as **Actions (Stocks)**, **Obligations (Bonds)**, and **Crypto**.
  - Automatic retrieval of purchase prices (if not provided) using historical data.
  - Update current market prices to compute real-time valuations. --> You need to specify binance key if you want crypto price to work

- **Portfolio Calculations:**  
  - Calculate the total portfolio value.
  - Compute Profit and Loss (PnL) per asset and in total.
  
- **Data Visualization:**  
  - Generate pie charts showing the distribution of the portfolio by asset class.

- **Import/Export:**  
  - Import portfolio data from an Excel file.
  - Export the current portfolio to Excel for record-keeping.
  - You have an exemple Excel file if you want a template

- **User Interface:**  
  - An intuitive Tkinter GUI to add, remove, view, and analyze portfolio assets.

## Requirements

- Python 3.6+
- [yfinance](https://pypi.org/project/yfinance/)
- [python-binance](https://pypi.org/project/python-binance/)
- [pandas](https://pypi.org/project/pandas/)
- [matplotlib](https://pypi.org/project/matplotlib/)
- Tkinter (usually included with Python)

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/portfolio-manager.git
   cd portfolio-manager

Usage
Adding an Asset:

Select the asset type from the dropdown (Action, Obligation, or Crypto).
Enter the asset’s name (symbol or ISIN), quantity, transaction date (YYYY-MM-DD), and optionally, the purchase price.
For obligations, provide the coupon rate.
Click on Ajouter Actif to add the asset to your portfolio.
Removing an Asset:

Enter the asset’s name and optionally the quantity to remove.
Click Supprimer Actif.
Viewing Valuation and PnL:

Click Afficher Valorisation Totale to see the current total portfolio value.
Click Calculer PnL to view the profit or loss for each asset as well as the overall portfolio.
Data Visualization:

Click Afficher Graphique to display a pie chart showing the distribution of your portfolio by asset class.
Importing/Exporting Data:

Use Importer Portefeuille to load asset data from an Excel file.
Use Exporter Portefeuille to save your current portfolio into an Excel file.
Code Structure
Classes:

Actif: Base class for all asset types.
Action: Handles stock-related assets using yfinance.
Obligation: Handles bonds with a simulated price update.
Crypto: Handles cryptocurrencies using the Binance API.
Portefeuille: Manages the collection of assets and portfolio calculations.
GUI:

Application: Tkinter-based interface for managing portfolio actions.
Additional helper functions for graphing and Excel file handling.
Contributing
Contributions are welcome! If you have suggestions or improvements, please open an issue or submit a pull request.

License
This project is open source and available under the MIT License.

Author
Nicolas ANNON
