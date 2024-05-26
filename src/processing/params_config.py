import json
import os
import logging
from typing import Dict, Any

def load_params(config_path: str = 'config/las_params.json') -> Dict[str, Dict[str, Any]]:
    """
    Load parameters from a JSON configuration file.

    Args:
        config_path (str, optional): Path to the JSON configuration file. Defaults to 'config/las_params.json'.

    Returns:
        Dict[str, Dict[str, Any]]: The loaded parameters.

    Raises:
        FileNotFoundError: If the configuration file does not exist.
        json.JSONDecodeError: If the configuration file is not a valid JSON.
    """
    if not os.path.exists(config_path):
        logging.error(f"Configuration file not found: {config_path}")
        raise FileNotFoundError(f"Configuration file not found: {config_path}")

    try:
        with open(config_path, 'r') as file:
            params = json.load(file)
        logging.info(f"Parameters successfully loaded from {config_path}")
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding JSON from configuration file: {config_path} - {e}")
        raise

    return params

def get_param_group(params: Dict[str, Dict[str, Any]], group_name: str) -> Dict[str, Any]:
    """
    Get a specific group of parameters from the loaded parameters.

    Args:
        params (Dict[str, Dict[str, Any]]): The loaded parameters.
        group_name (str): The name of the parameter group to retrieve.

    Returns:
        Dict[str, Any]: The parameter group.

    Raises:
        KeyError: If the parameter group is not found.
    """
    try:
        param_group = params[group_name]
        logging.info(f"Parameter group '{group_name}' successfully retrieved.")
        return param_group
    except KeyError:
        logging.error(f"Parameter group '{group_name}' not found in the parameters.")
        raise

# Load the parameters from the configuration file
params = load_params()

# Access specific parameter groups
LASINFO_PARAMS = get_param_group(params, "LASINFO_PARAMS")

# Add more parameter groups as needed
# LASCLASSIFY_PARAMS = get_param_group(params, "LASCLASSIFY_PARAMS")
