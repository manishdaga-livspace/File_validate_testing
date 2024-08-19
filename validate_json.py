import json
import sys
import logging

# Configure logging
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def verify_dict(dict_value, required_cols, forbidden_audit_cols):
    missing_keys = [col for col in required_cols if col not in dict_value]
    if missing_keys:
        error_message = f"Missing required keys: {', '.join(missing_keys)} in {dict_value}"
        print(f"Error: {error_message}")
        logger.error(error_message)
        sys.exit(1)

    empty_keys = [col for col in required_cols if dict_value.get(col) in [None, ""]]
    if empty_keys:
        error_message = f"Required keys {', '.join(empty_keys)} have empty or null values in {dict_value}"
        print(f"Error: {error_message}")
        logger.error(error_message)
        sys.exit(1)

    if 'audit_column' in dict_value:
        forbidden_in_audit = [col for col in forbidden_audit_cols if col in dict_value['audit_column']]
        if forbidden_in_audit:
            error_message = f"Unwanted columns {', '.join(forbidden_in_audit)} found in audit_column of {dict_value}"
            print(f"Error: {error_message}")
            logger.error(error_message)
            sys.exit(1)

    return True

def main():
    if len(sys.argv) != 2:
        print("Usage: python validate_json.py <path_to_json>")
        sys.exit(1)

    json_file_path = sys.argv[1]

    try:
        with open(json_file_path, 'r') as file:
            data = json.load(file)
    except json.JSONDecodeError as e:
        error_message = f"Failed to decode JSON file. Error: {e}"
        print(f"Error: {error_message}")
        logger.error(error_message)
        sys.exit(1)
    except FileNotFoundError as e:
        error_message = f"File not found. Error: {e}"
        print(f"Error: {error_message}")
        logger.error(error_message)
        sys.exit(1)

    required_columns = [
        "rds_name", "rds_instance_type", "db_name", 
        "tb_name", "primaryKey", "audit_column", "date_column"
    ]

    forbidden_audit_columns = [
        "updated_at", "updated_by", "updated_by_id", "updated_ts_dms"
    ]

    if isinstance(data, list):
        for item in data:
            if not isinstance(item, dict):
                error_message = f"List item is not a dictionary: {item}"
                print(f"Error: {error_message}")
                logger.error(error_message)
                sys.exit(1)
            verify_dict(item, required_columns, forbidden_audit_columns)
    elif isinstance(data, dict):
        verify_dict(data, required_columns, forbidden_audit_columns)
    else:
        error_message = "Invalid JSON structure. Must be a list or dictionary."
        print(f"Error: {error_message}")
        logger.error(error_message)
        sys.exit(1)

if __name__ == "__main__":
    main()
