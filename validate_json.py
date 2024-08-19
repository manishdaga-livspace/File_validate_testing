import json
import logging
import sys

class Validate:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def verify_dict(self, dict_value, default_col, primary_col):
        try:
            for col in default_col:
                if col not in dict_value.keys():
                    raise ValueError(f'Missing {col} in {dict_value}')

            if 'audit_column' in dict_value:
                for col in primary_col:
                    if col in dict_value['audit_column']:
                        raise ValueError(f'Unwanted {col} found in audit_column of {dict_value}')

        except ValueError as e:
            self.send_error_mail(e)
            self.logger.error(e)
            sys.exit(1)  # Exit with an error code if validation fails
        except Exception as e:
            self.send_error_mail(e)
            self.logger.error(e)
            sys.exit(1)  # Exit with an error code if there is an exception

        return True

    def send_error_mail(self, error_message):
        # Placeholder for email sending functionality
        print(f"Sending error email: {error_message}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python validate_json.py <path_to_json>")
        sys.exit(1)

    json_file_path = sys.argv[1]

    with open(json_file_path, 'r') as file:
        data = json.load(file)

    default_columns = ["key1", "key2"]  # Update with your required keys
    primary_columns = ["key3"]          # Update with your audit columns

    validator = Validate()
    validator.verify_dict(data, default_columns, primary_columns)
