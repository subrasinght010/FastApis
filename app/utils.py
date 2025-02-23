import pandas as pd

def validate_csv(file_path: str) -> tuple[bool, str]:
    """ Validates the CSV format. """
    try:
        df = pd.read_csv(file_path)

        # Required columns check
        required_columns = {"Serial Number", "Product Name", "Input Image Urls"}
        if not required_columns.issubset(df.columns):
            return False, f"CSV must contain {required_columns} columns"

        # Check if input URLs are valid
        if df["Input Image Urls"].isnull().any():
            return False, "Missing input image URLs in CSV"

        return True, "CSV is valid"

    except Exception as e:
        return False, f"Error reading CSV: {str(e)}"
