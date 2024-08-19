import json
import logging
import sys

class Validate:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def verify_dict(self, dict_value, required_cols, forbidden_audit_cols):
        try:
            # Check for required keys
            for col in required_cols:
                if col not in dict_value:
                    raise ValueError(f'Missing required key: {col} in {dict_value}')

            # Check for forbidden values in audit_column
            if 'audit_column' in dict_value:
                for col in forbidden_audit_cols:
                    if col in dict_value['audit_column']:
                        raise ValueError(f'Unwanted {col} found in audit_column of {dict_value}')

        except ValueError as e:
            self.logger.error(e)
            print(e)
            sys.exit(1)  # Exit with an error code if validation fails
        except Exception as e:
            self.logger.error(e)
            print(e)
            sys.exit(1)  # Exit with an error code if there is an exception

        return True

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python validate_json.py <path_to_json>")
        sys.exit(1)

    json_file_path = sys.argv[1]

    with open(json_file_path, 'r') as file:
        data = json.load(file)

    # List of required columns
    required_columns = [
        "rds_name", "rds_instance_type", "db_name", 
        "tb_name", "primaryKey", "audit_column", "date_column"
    ]
    
    # List of forbidden columns in audit_column
    forbidden_audit_columns = [
        "updated_at", "updated_by", "updated_by_id", "updated_ts_dms"
    ]

    validator = Validate()

    if isinstance(data, list):
        # Iterate over each dictionary in the list
        for item in data:
            validator.verify_dict(item, required_columns, forbidden_audit_columns)
    elif isinstance(data, dict):
        # Handle the case where the top-level JSON is a dictionary
        validator.verify_dict(data, required_columns, forbidden_audit_columns)
    else:
        print("Invalid JSON structure: must be a list or dictionary.")
        sys.exit(1)
