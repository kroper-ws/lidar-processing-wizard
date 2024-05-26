import logging
import configparser
import os
from typing import Optional
import sys


def load_config(config_path: str = 'config/config.ini') -> configparser.ConfigParser:
    """
    Load configuration from the specified path.

    Args:
        config_path (str, optional): Path to the configuration file. Defaults to 'config/config.ini'.

    Returns:
        configparser.ConfigParser: The loaded configuration.

    Raises:
        FileNotFoundError: If the configuration file does not exist.
    """
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found: {config_path}")

    config = configparser.ConfigParser()
    config.read(config_path)
    return config


def setup_logging(log_directory: str, log_file: str, log_level: Optional[str] = 'INFO') -> logging.Logger:
    """
    Set up logging configuration.

    Args:
        log_directory (str): Directory to store log files.
        log_file (str): Name of the log file.
        log_level (str, optional): Logging level. Defaults to 'INFO'.

    Returns:
        logging.Logger: Configured logger instance.
    """
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    log_path = os.path.join(log_directory, log_file)

    logging.basicConfig(
        level=getattr(logging, log_level.upper(), logging.INFO),
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_path),
            logging.StreamHandler(sys.stdout)
        ]
    )

    logger = logging.getLogger()
    return logger


def validate_config(config: configparser.ConfigParser, sections: dict) -> None:
    """
    Validate the presence of required sections and keys in the configuration.

    Args:
        config (configparser.ConfigParser): The configuration to validate.
        sections (dict): A dictionary where keys are section names and values are lists of required keys.

    Raises:
        ValueError: If a required section or key is missing.
    """
    for section, keys in sections.items():
        if section not in config:
            raise ValueError(f"Missing section in configuration file: {section}")
        for key in keys:
            if key not in config[section]:
                raise ValueError(f"Missing key in section '{section}': {key}")
