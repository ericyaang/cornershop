# Cornershop API Data Extraction Tool

This Python script is designed to fetch product data from the Cornershop API and save it in a JSON file. It retrieves product data based on a user-specified product name, postal code, and country code.

## Dependencies

The script relies on these Python libraries:

- requests
- logging
- datetime
- typing
- json
- os

## Features

- Extracts product data from the Cornershop API
- Transforms the fetched data into a format suitable for a DataFrame
- Saves the transformed data as a JSON file in the specified directory

## Usage

Before running the script, replace the `term`, `code`, and `country` variables with your desired product name, postal code, and country code, respectively. 

You also need to set base_dir to your desired directory path where the JSON file should be saved.

```python
term = 'sabonete'  # replace with your product name
code = 88010560  # replace with your postal code
country = 'BR'  # replace with your country code
base_dir = r'C:\Users\User\Your Directory'
```

Then run the script. It will fetch data from the Cornershop API, transform it, and save it in the specified directory as a JSON file named {term}_{code}_{current_timestamp}.json.

## Main Functions

The script includes these main functions:
#### `get_product_data(query: str, cep: int, country: str) -> dict`

Fetches product data from the Cornershop API based on the provided product name, postal code, and country code, and returns a dictionary containing the search results.

#### `create_data(results: List[Dict])`
Takes a list of dictionaries, which are the search results from get_product_data, and transforms it into a list of dictionaries ready for a DataFrame.

#### `get_and_create(term, code, country, base_dir)`
This is the main function that calls get_product_data, transforms the fetched data using create_data, and saves the transformed data as a JSON file in the specified directory. It also prints out messages during the process to inform the user of the current status.

## Contribution

Contributions are welcome. Please ensure that your code adheres to Python's best practices.