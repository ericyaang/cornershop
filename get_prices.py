import requests
from typing import Optional
import logging
import json
import argparse
import pandas as pd
import datetime
import os


def get_product_data(query: str, cep: int, country: str) -> Optional[dict]:
    """
    Fetches product data from the Cornershop API.

    Parameters
    ----------
    query : str
        Name of the product to search for.
    cep : int
        Postal code.
    country : str
        Country code.

    Returns
    -------
    json_file : dict or None
        JSON object containing the search results or None if an error occurred.
    """
    URL = "https://cornershopapp.com/api/v2/branches/search"
    HEADERS = {"User-Agent": "Mozilla/5.0"}

    params = {"query": query, "locality": cep, "country": country}

    try:
        response = requests.get(URL, params=params, headers=HEADERS)
        response.raise_for_status()  # Raise an exception if the response indicates an unsuccessful status
        json_file = response.json()
        return json_file
    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        logging.error(f"Other Requests error occurred: {req_err}")

    return None


def dump_to_file(data: dict, filename: str):
    """
    Dumps the data to a JSON file.

    Parameters
    ----------
    data : dict
        Data to be dumped.
    filename : str
        Name of the file where the data will be dumped.
    """
    try:
        with open(filename, "w") as f:
            json.dump(data, f)
        print(f"Data successfully dumped to {filename}")
    except Exception as e:
        print(f"An error occurred while dumping data to the file: {e}")


def create_dataframe(results):
    """
    Create a dataframe from the given results.

    Parameters
    ----------
    results : list
        List of dictionaries containing store and product details.

    Returns
    -------
    df : DataFrame
        DataFrame containing store and product details.
    """

    def create_row(data, aisle, product):
        """
        Create a dictionary for a single row in the dataframe.
        """

        return {
            "Date": datetime.date.today().isoformat(),
            "Product Price": product.get("pricing", {})
            .get("price", {})
            .get("amount", ""), 
            "Package": product.get("package", ""),                                            
            #'Store Description': data.get('store', {}).get('description', ''),
            "Search Term": data.get("search_result", {}).get("search_term", ""),
            "Brand": product.get("brand", []).get("name", ""),
            "Brand ID": product.get("brand", []).get("id", ""),
            "Aisle Name": aisle.get("aisle_name", ""),
            "Product Name": product.get("name", ""),
            "Product ID": product.get("id", ""),
            "Store Name": data.get("store", {}).get("name", ""),
            "Store ID": data.get("store", {}).get("id", ""),
            "Store City": data.get("store", {})
            .get("closest_branch", {})
            .get("city", ""),            
        }

    rows = [
        create_row(data, aisle, product)
        for data in results
        for aisle in data.get("search_result", {}).get("aisles", [])
        for product in aisle.get("products", [])
    ]

    df = pd.DataFrame(rows)
    return df


def export_data(df: pd.DataFrame, dir_path: str, base_name: str, format: str) -> None:
    """
    Exports the data to a specific file format.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame to be exported.
    dir_path : str
        Directory path where the file will be exported.
    base_name : str
        Base name of the file to be exported.
    format : str
        Format of the output file.
    """
    supported_formats = {"csv", "parquet", "json"}

    # Check for supported file format
    if format not in supported_formats:
        raise ValueError(
            f"Unsupported file format: {format}. Supported formats are {supported_formats}."
        )

    # Create the directory if it does not exist
    os.makedirs(dir_path, exist_ok=True)

    try:
        # Add current timestamp to the filename
        timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        filename = f"{base_name}_{timestamp}.{format}"

        # Create full file path
        file_path = os.path.join(dir_path, filename)

        if format == "csv":
            df.to_csv(file_path, index=False)
        elif format == "parquet":
            df.to_parquet(file_path, index=False)
        elif format == "json":
            df.to_json(file_path, orient="records", lines=True)

        logging.info(f"Data successfully exported to {file_path}")
    except Exception as e:
        logging.error(f"An error occurred while exporting data to {file_path}: {e}")
        raise


def fetch_and_export_product_data(
    query: str, cep: int, country: str, dir_path: str, base_name: str, format: str
) -> None:
    """
    Fetches product data from the Cornershop API and exports it to a specified file format.

    Parameters
    ----------
    query : str
        Name of the product to search for.
    cep : int
        Postal code.
    country : str
        Country code.
    dir_path : str
        Directory path where the file will be exported.
    base_name : str
        Base name of the file to be exported.
    format : str
        Format of the output file.
    """
    # Fetch raw JSON data
    raw_json_data = get_product_data(query, cep, country)
    if not raw_json_data:
        logging.warning("No data returned.")
        return

    # Extract 'results' from raw JSON data
    product_results = raw_json_data.get("results", [])
    if not isinstance(product_results, list):
        logging.warning("'results' is not present or not a list in the returned data.")
        return

    # Create a dataframe from product results
    df = create_dataframe(product_results)

    # Export data
    export_data(df, dir_path, base_name, format)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch and export product data.")
    parser.add_argument(
        "--query", required=True, type=str, help="Product to search for."
    )
    parser.add_argument("--cep", required=True, type=int, help="Postal code.")
    parser.add_argument("--country", required=True, type=str, help="Country code.")
    parser.add_argument(
        "--dir_path", required=True, type=str, help="Directory path to export data to."
    )
    parser.add_argument(
        "--base_name",
        required=True,
        type=str,
        help="Base name of the file to be exported.",
    )
    parser.add_argument(
        "--format", required=True, type=str, help="Format of the output file."
    )

    args = parser.parse_args()

    fetch_and_export_product_data(
        args.query, args.cep, args.country, args.dir_path, args.base_name, args.format
    )


# python get_prices.py --query "amaciante" --cep 88010560 --country "BR" --dir_path "./data/" --base_name "product_data" --format "csv"
