import pandas as pd
import os

def load_data(college_type):
    """
    Loads and cleans the college cutoff data from the specified CSV files.
    Returns a combined DataFrame.
    """
    if college_type == "IIT":
        files = {
            "OPEN": "data/OPEN_Cat_Forms_Kart.csv",
            "OBC-NCL": "data/OBC_NCL_Forms_Kart_2024_IIT.csv",
            "EWS": "data/EWS_Cat_Forms_Kart_IIT_24.csv",
            "ST": "data/ST_Category_IIT_2024_Forms_kart.csv",
            "SC": "data/SC_Data_IIT_2024.csv"
        }
    else:
        files = {
            "OPEN": "data/OS_Only_NIT_Open_Cat.csv",
            "EWS": "data/OS_NITs_EWS_Cat.csv",
            "OBC-NCL": "data/NITs_OS_OBC_NCL.csv",
            "SC": "data/SC_NIT_OS.csv",
            "ST": "data/OS_NITs_ST.csv"
        }

    combined_data = pd.DataFrame()
    for category, file_path in files.items():
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Data file not found: {file_path}")

        data = pd.read_csv(file_path)
        print(f"Loading data from: {file_path}")  # Debug info
        
        # Standardize column names
        data.columns = data.columns.str.strip().str.title()
        data.rename(columns={
            "Institute": "institute",
            "Academic Program Name": "branch",
            "Seat Type": "seat_type",
            "Gender": "gender",
            "Opening Rank": "opening_rank",
            "Closing Rank": "closing_rank"
        }, inplace=True)
        
        # Convert ranks to numeric and clean
        data["closing_rank"] = pd.to_numeric(data["closing_rank"], errors="coerce")
        data["opening_rank"] = pd.to_numeric(data["opening_rank"], errors="coerce")
        data.dropna(subset=["closing_rank", "opening_rank"], inplace=True)
        
        # Validate seat types
        data["seat_type"] = data["seat_type"].str.upper().str.strip()
        
        # Add category information
        data["category"] = category
        
        # Debug info for loaded data
        print(f"Loaded {len(data)} records from {category}")
        print(f"Sample seat types: {data['seat_type'].unique()}")
        
        combined_data = pd.concat([combined_data, data], ignore_index=True)

    return combined_data
