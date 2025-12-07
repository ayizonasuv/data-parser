import json
import logging
import os
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

def read_json_file(file_path: str) -> Optional[Dict[str, Any]]:
    """
    Reads a JSON file and returns its content as a dictionary.
    Returns None if the file does not exist or if an error occurs during reading/parsing.
    """
    if not os.path.exists(file_path):
        logger.error(f"File not found: {file_path}")
        return None

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON in file {file_path}: {e}")
        return None
    except Exception as e:
        logger.exception(f"An unexpected error occurred while reading {file_path}: {e}")
        return None

def write_json_file(file_path: str, data: Dict[str, Any], indent: int = 4) -> bool:
    """
    Writes data to a JSON file.

    Args:
        file_path: The path to the JSON file.
        data: The data to write (must be serializable to JSON).
        indent: The indentation level for the JSON file.

    Returns:
        True if the write was successful, False otherwise.
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=indent, ensure_ascii=False)
        return True
    except TypeError as e:
        logger.error(f"Error serializing data to JSON for file {file_path}: {e}")
        return False
    except Exception as e:
        logger.exception(f"An unexpected error occurred while writing to {file_path}: {e}")
        return False

def validate_data(data: Dict[str, Any], schema: Dict[str, Any]) -> List[str]:
    """
    Validates data against a schema.  This is a very basic implementation.
    For more robust validation, consider using a library like `jsonschema`.

    Args:
        data: The data to validate.
        schema: A simplified schema defining required keys and their types.
               Example: {"name": str, "age": int, "is_active": bool}

    Returns:
        A list of error messages.  If the list is empty, the data is valid.
    """
    errors: List[str] = []
    for key, expected_type in schema.items():
        if key not in data:
            errors.append(f"Missing required key: {key}")
        elif not isinstance(data[key], expected_type):
            errors.append(f"Key '{key}' should be of type {expected_type}, but is {type(data[key])}")
    return errors