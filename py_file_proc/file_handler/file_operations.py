# your_project_name/file_handler/file_operations.py

import os
import csv
import json
from lxml import etree # New import for XML handling
from datetime import datetime # New import for timestamp
from your_project_name.config import settings

def get_output_filepath(filename: str = settings.OUTPUT_FILE_NAME) -> str:
    """Constructs the full path for the output file."""
    return os.path.join(settings.OUTPUT_FILE_DIRECTORY, filename)

def create_csv_file(data: list, filename: str = settings.OUTPUT_FILE_NAME) -> str | None:
    """
    Creates a CSV file from a list of dictionaries.

    Args:
        data (list): A list of dictionaries, where each dictionary is a row.
        filename (str): The name of the CSV file to create.

    Returns:
        str | None: The full path to the created file if successful, None otherwise.
    """
    if not data:
        print("No data provided to create CSV file.")
        return None

    filepath = get_output_filepath(filename)
    keys = data[0].keys() # Assumes all dicts have the same keys

    try:
        with open(filepath, 'w', newline='', encoding='utf-8') as output_file:
            dict_writer = csv.DictWriter(output_file, fieldnames=keys)
            dict_writer.writeheader()
            dict_writer.writerows(data)
        print(f"CSV file created successfully at: {filepath}")
        return filepath
    except IOError as e:
        print(f"Error creating CSV file {filepath}: {e}")
        return None

def create_json_file(data: list, filename: str = "data_export.json") -> str | None:
    """
    Creates a JSON file from a list of dictionaries.

    Args:
        data (list): A list of dictionaries.
        filename (str): The name of the JSON file to create.

    Returns:
        str | None: The full path to the created file if successful, None otherwise.
    """
    if not data:
        print("No data provided to create JSON file.")
        return None

    filepath = get_output_filepath(filename)

    try:
        with open(filepath, 'w', encoding='utf-8') as output_file:
            json.dump(data, output_file, indent=4)
        print(f"JSON file created successfully at: {filepath}")
        return filepath
    except IOError as e:
        print(f"Error creating JSON file {filepath}: {e}")
        return None

def create_xml_file_from_template(data: list, output_filename: str = "data_export.xml") -> str | None:
    """
    Creates an XML file from a list of dictionaries using a predefined template.

    The template is expected to have a '<records>' element where individual
    '<record>' elements (representing each row of data) will be appended.
    Metadata like 'current_timestamp' in the template will be replaced.

    Args:
        data (list): A list of dictionaries, where each dictionary is a row.
        output_filename (str): The name of the XML file to create.

    Returns:
        str | None: The full path to the created file if successful, None otherwise.
    """
    if not data:
        print("No data provided to create XML file.")
        return None

    template_filepath = os.path.join(
        os.path.dirname(__file__), settings.XML_TEMPLATE_FILE_NAME
    )
    if not os.path.exists(template_filepath):
        print(f"XML template file not found: {template_filepath}")
        return None

    output_filepath = get_output_filepath(output_filename)

    try:
        # Parse the XML template
        parser = etree.XMLParser(remove_blank_text=True) # Remove whitespace-only text nodes
        tree = etree.parse(template_filepath, parser)
        root = tree.getroot()

        # Replace placeholders in metadata
        timestamp_element = root.find(".//generated_at")
        if timestamp_element is not None:
            timestamp_element.text = datetime.now().isoformat()

        # Find the <records> element to append data
        records_element = root.find(".//records")
        if records_element is None:
            print("Error: '<records>' element not found in XML template.")
            return None

        # Populate the <records> element with data
        for row_dict in data:
            record_element = etree.SubElement(records_element, "record")
            for key, value in row_dict.items():
                field_element = etree.SubElement(record_element, key)
                field_element.text = str(value) # Convert all values to string

        # Write the modified XML to the output file
        with open(output_filepath, 'wb') as f: # 'wb' for binary write with etree
            f.write(etree.tostring(tree, pretty_print=True, encoding='utf-8', xml_declaration=True))

        print(f"XML file created successfully at: {output_filepath}")
        return output_filepath
    except etree.XMLSyntaxError as e:
        print(f"Error parsing XML template: {e}")
        return None
    except IOError as e:
        print(f"Error creating XML file {output_filepath}: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred during XML creation: {e}")
        return None

# Example usage
if __name__ == "__main__":
    sample_data = [
        {"id": 1, "name": "Alice", "age": 30},
        {"id": 2, "name": "Bob", "age": 24},
        {"id": 3, "name": "Charlie", "age": 35}
    ]
    csv_path = create_csv_file(sample_data, "sample_data.csv")
    json_path = create_json_file(sample_data, "sample_data.json")
    xml_path = create_xml_file_from_template(sample_data, "sample_data.xml") # New example

    if csv_path:
        print(f"CSV file available at: {csv_path}")
    if json_path:
        print(f"JSON file available at: {json_path}")
    if xml_path:
        print(f"XML file available at: {xml_path}")