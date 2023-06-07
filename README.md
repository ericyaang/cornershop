# Cornershop Product Data Fetcher

This script fetches product data from the Cornershop API and exports the results to a specified file format (csv, parquet or json).

## Requirements

- Python 3.7 or later
- pandas
- requests
- os, argparse, json, logging, datetime modules (standard in Python 3)

## Usage

1. Clone this repository to your local machine.
2. Install the required libraries by running `pip install pandas requests` in your terminal.
3. Run the script from the command line by specifying the necessary arguments:

```bash
python cornershop_product_data_fetcher.py --query "query" --cep "cep" --country "country_code" --dir_path "directory_path" --base_name "base_name" --format "file_format"
```

Here, replace "query" with your product search term, "cep" with your postal code, "country_code" with your country code (like "US", "BR", etc.), "directory_path" with the path where you want to save the file, "base_name" with the base name for the output file, and "file_format" with the file format ("csv", "parquet" or "json").

For example, you might run something like this:

```bash
python cornershop_product_data_fetcher.py --query "apple" --cep 12345 --country "US" --dir_path "./data" --base_name "products" --format "csv"
```
This will search for "apple" in the Cornershop database, and save the resulting data in the file named something like products_20230705-103000.csv in the ./data directory.


Remember to replace `cornershop_product_data_fetcher.py` with the actual filename of your script. This README assumes that all the provided code is placed in one Python file.

You might want to add more information about the data returned from the Cornershop API and stored in the exported file, instructions for how to interpret it, and other relevant information for users of your script.
