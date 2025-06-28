import pandas as pd
import os

# Helper Function: Load and Clean Data
def load_data(college_type):
    """
    Loads and cleans the college cutoff data from the specified CSV files.
    Returns a combined DataFrame.
    """
    if college_type == "IIT":
        # File paths for IIT categories
        files = {
            "OPEN": "OPEN_Cat_Forms_Kart.csv",
            "OBC-NCL": "OBC_NCL_Forms_Kart_2024_IIT.csv",
            "EWS": "EWS_Cat_Forms_Kart_IIT_24.csv",
            "ST": "ST_Category_IIT_2024_Forms_kart.csv",
            "SC": "SC_Data_IIT_2024.csv"
        }
    else:
        # File paths for NIT categories
        college_type == "NIT":
        files = {
            "OPEN": "OS_Only_NIT_Open_Cat.csv",
            "EWS": "OS_NITs_EWS_Cat.csv",
            "OBC-NCL": "NITs_OS_OBC_NCL.csv",
            "ST": "OS_NITs_ST.csv",
            "SC": "SC_NIT_OS.csv"
            
            }
     elif:
        college_type == "Indian Institute of Information Technology (IIIT)":
        files = {
             "OPEN": " ",
            "OBC-NCL": " ",
            "EWS": " ",
            "ST": " ",
            "SC": " "

    # Load data for all categories
    combined_data = pd.DataFrame()
    for category, file_path in files.items():
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Data file not found: {file_path}")

        data = pd.read_csv(file_path)
        data.dropna(inplace=True)
        data.rename(columns={
            "Institute": "institute",
            "Academic Program Name": "branch",  # Renaming column
            "Seat Type": "seat_type",
            "Gender": "gender",
            "Opening Rank": "opening_rank",
            "Closing Rank": "closing_rank"
        }, inplace=True)

        # Convert 'closing_rank' and 'opening_rank' to numeric
        data["closing_rank"] = pd.to_numeric(data["closing_rank"], errors="coerce")
        data["opening_rank"] = pd.to_numeric(data["opening_rank"], errors="coerce")

        # Drop rows where 'closing_rank' or 'opening_rank' is NaN
        data.dropna(subset=["closing_rank", "opening_rank"], inplace=True)

        # Convert ranks to integers
        data["closing_rank"] = data["closing_rank"].astype(int)
        data["opening_rank"] = data["opening_rank"].astype(int)

        # Add category information
        data["category"] = category

        # Append to combined data
        combined_data = pd.concat([combined_data, data], ignore_index=True)

    return combined_data
