import pandas as pd
import json

# Path to your Excel file
input_file_path = 'final_dataframe.xlsx'
# Path to the output JSONL file
output_file_path = 'ab.jsonl'

# Read the Excel file
df = pd.read_excel(input_file_path)

# Open the JSONL file for writing
with open(output_file_path, 'w', encoding='utf-8') as jsonl_file:
    # Iterate over the rows of the DataFrame
    for index, row in df.iterrows():
        # Check if both 'judgment' and 'summary' columns exist, are not NaN, and are non-empty strings
        if pd.notna(row['judgment']) and isinstance(row['judgment'], str) and len(row['judgment'].strip()) > 0 \
           and pd.notna(row['summary']) and isinstance(row['summary'], str) and len(row['summary'].strip()) > 0:
            # Create a JSON record as a message object with a prompt and completion
            json_record = {
                "prompt": "Act as a legal assistant and generate a summary of the following legal document: " + row['judgment'].strip(),
                "completion": row['summary'].strip()
            }
            # Write the JSON record to the file, followed by a newline character
            jsonl_file.write(json.dumps(json_record) + '\n')
