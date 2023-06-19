import requests
import logging
from datetime import datetime
from typing import Any, Dict, List
from time import sleep
import json
import os


class APIError(Exception):
    """Custom exception for API errors."""

    pass


def get_product_data(query: str, cep: int, country: str) -> dict:
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
    dict
        JSON object containing the search results.

    Raises
    ------
    APIError
        If there is an error with the request or response.
    """
    URL = "https://cornershopapp.com/api/v2/branches/search"
    HEADERS = {"User-Agent": "Mozilla/5.0"}

    params = {"query": query, "locality": cep, "country": country}

    try:
        sleep(2)  # Resonable interval betwween requests
        response = requests.get(URL, params=params, headers=HEADERS)
        response.raise_for_status()
    except (requests.exceptions.HTTPError, requests.exceptions.RequestException) as err:
        logging.error(f"Error occurred while fetching product data: {err}")
        raise APIError("An error occurred while fetching product data.") from err

    try:
        return response.json()
    except ValueError:
        raise APIError("Received an invalid JSON response.")


##--- helper functions for create_data --- ##


def get_nested(data: Dict, *args: str) -> Any:
    """
    Safely navigates a nested dictionary.
    """
    for arg in args:
        if data is None:
            return None
        data = data.get(arg)
    return data


def create_row(data: Dict, aisle: Dict, product: Dict) -> Dict:
    """
    Create a dictionary for a single row in the dataframe.
    """
    return {
        "date": datetime.today().strftime("%d-%m-%Y"),
        "aisle_name": aisle.get("aisle_name", None),
        "product_name": product.get("name", None),
        "brand": get_nested(product, "brand", "name"),
        "price": get_nested(product, "pricing", "price", "amount"),
        "package": product.get("package", None),
        "store_name": get_nested(data, "store", "name"),
        "store_city": get_nested(data, "store", "closest_branch", "city"),
        "search_term": get_nested(data, "search_result", "search_term"),
    }


def create_data(results: List[Dict]):
    """
    Create a ready dataframe format from the given results.
    """
    rows = [
        create_row(data, aisle, product)
        for data in results
        for aisle in get_nested(data, "search_result", "aisles")
        for product in aisle.get("products", [])
    ]
    return rows


def save_as_json(data, save_path):
    with open(save_path, "w") as file:
        json.dump(data, file)


def get_and_create(term, code, country, base_dir):
    """
    Get the product data and optionally save it as a JSON file.

    Parameters
    ----------
    term : str
        The term for which to get product data.
    code : int
        The code to use when getting product data.
    country : str
        The country to use when getting product data.
    save_path : str, optional
        The file path where the JSON file should be saved.

    Returns
    -------
    data : list
        The transformed data.
    """
    print("Fetching product data...")
    raw_json_data = get_product_data(term, code, country)
    json_data = raw_json_data.get("results", [])
    data = create_data(json_data)

    data_dir = os.path.join(base_dir, "data")
    os.makedirs(data_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{term}_{code}_{timestamp}"
    save_path = os.path.join(data_dir, f"{filename}.json")
    print(f"Saving data as JSON: {save_path}")
    save_as_json(data, save_path)
    print("Data saved successfully.")
    return data


if __name__ == "__main__":
    from listas import supermercado
    
    base_dir = os.getenv("CS_DIRECTORY")
    code = os.getenv("CS_CODE")
    country = os.getenv("CS_COUNTRY")

    for categoria in supermercado:
        for item in categoria:
            fruta_data = get_and_create(item, code, country, base_dir)
