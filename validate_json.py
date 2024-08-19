import json
import sys

def verify_dict(dict_value, required_cols, forbidden_audit_cols):
    for col in required_cols:
        if col not in dict_value:
            print(f"Error: Missing required key: {col} in {dict_value}")
            sys.exit(1)
        if dict_value[col] in [None, ""]:
            print(f"Error: Required key {col} has an empty or null value in {dict_value}")
            sys.exit(1)
    
    if 'audit_column' in dict_value:
        for col in forbidden_audit_cols:
            if col in dict_value['audit_column']:
                print(f"Error: Unwanted {col} found in audit_column of {dict_value}")
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
        print(f"Error: Failed to decode JSON file. {e}")
        sys.exit(1)
    except FileNotFoundError as e:
        print(f"Error: File not found. {e}")
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
                print(f"Error: List item is not a dictionary: {item}")
                sys.exit(1)
            verify_dict(item, required_columns, forbidden_audit_columns)
    elif isinstance(data, dict):
        verify_dict(data, required_columns, forbidden_audit_columns)
    else:
        print("Error: Invalid JSON structure. Must be a list or dictionary.")
        sys.exit(1)

if __name__ == "__main__":
    main()
