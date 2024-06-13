import json
import csv

def jsonl_to_csv(jsonl_filename, csv_filename):
    with open(jsonl_filename, 'r') as json_file, open(csv_filename, 'w', newline='') as csv_file:
        fieldnames = set()
        data = []

        # Read each line in the JSONL file
        for line in json_file:
            record = json.loads(line)

            # Collect field names
            fieldnames.update(record.keys())

            # Append record to data list
            data.append(record)

        # Create a CSV writer with fieldnames
        csv_writer = csv.DictWriter(csv_file, fieldnames=list(fieldnames))

        # Write header row to CSV file
        csv_writer.writeheader()

        # Write data to CSV file
        csv_writer.writerows(data)

# Example usage
jsonl_to_csv("outputs/tabfact_rc_nov12_A.jsonl", "tabfact_rc_final-err_analysis.csv")
