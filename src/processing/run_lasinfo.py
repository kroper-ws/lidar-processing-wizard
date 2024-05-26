import subprocess
import logging
from typing import Any, Dict


def run_lasinfo(input_path: str, **params: Any) -> str:
    """
    Run the lasinfo command with specified parameters on the input file.

    Args:
        input_path (str): Path to the input LAS file.
        params (dict): Additional parameters for the lasinfo command.

    Returns:
        str: Output from the lasinfo command.

    Raises:
        subprocess.CalledProcessError: If the lasinfo command fails.
    """
    command = ['lasinfo', '-i', input_path]

    for param, value in params.items():
        if isinstance(value, bool) and value:
            command.append(f'-{param}')
        elif isinstance(value, list):
            command.append(f'-{param}')
            command.extend(map(str, value))
        else:
            command.append(f'-{param}')
            command.append(str(value))

    logging.info(f"Running command: {' '.join(command)}")

    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        logging.info("Command executed successfully")
        return result.stderr  # Capturing stderr instead of stdout
    except subprocess.CalledProcessError as e:
        logging.error(f"Command failed with error: {e.stderr}")
        raise


if __name__ == "__main__":
    import sys
    logging.basicConfig(level=logging.INFO)

    if len(sys.argv) < 2:
        print("Usage: python run_lasinfo.py <input_path> [param1=value1 param2=value2 ...]")
        sys.exit(1)

    input_path = sys.argv[1]
    params = {}
    for arg in sys.argv[2:]:
        if '=' in arg:
            key, value = arg.split('=', 1)
            params[key] = value.split() if ' ' in value else value
        else:
            params[arg] = True

    try:
        output = run_lasinfo(input_path, **params)
        print(output)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)
