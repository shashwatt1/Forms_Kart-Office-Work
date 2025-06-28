import pandas as pd
import os

def load_data(college_type):
    if college_type == "Indian Institute of Technology (IIT)":
        files = {
            "OPEN": "OPEN_Cat_Forms_Kart.csv",
            "OBC-NCL": "OBC_NCL_Forms_Kart_2024_IIT.csv",
            "EWS": "EWS_Cat_Forms_Kart_IIT_24.csv",
            "ST": "ST_Category_IIT_2024_Forms_kart.csv",
            "SC": "SC_Data_IIT_2024.csv"
        }
    elif college_type == "National Institute of Technology (NIT)":
        files = {
            "OPEN": "OS_Only_NIT_Open_Cat.csv",
            "EWS": "OS_NITs_EWS_Cat.csv",
            "OBC-NCL": "NITs_OS_OBC_NCL.csv",
            "ST": "OS_NITs_ST.csv",
            "SC": "SC_NIT_OS.csv"
        }
    elif college_type == "Indian Institute of Information Technology (IIIT)":
        files = {
            "OPEN": "OPEN_IIIT_2024.csv",
            "OBC-NCL": "OBC_IIIT_2024.csv",
            "EWS": "EWS_IIIT_2024.csv",
            "ST": "ST_IIIT_2024.csv",
            "SC": "SC_IIIT_2024.csv"
        }
    else:
        raise ValueError("Unsupported college type")

    combined_data = pd.DataFrame()
    for category, file_path in files.items():
        if not os.path.exists(file_path):
            continue
        df = pd.read_csv(file_path)
        df.dropna(inplace=True)
        df.rename(columns={
            "Institute": "institute",
            "Academic Program Name": "branch",
            "Seat Type": "seat_type",
            "Gender": "gender",
            "Opening Rank": "opening_rank",
            "Closing Rank": "closing_rank"
        }, inplace=True)
        df["closing_rank"] = pd.to_numeric(df["closing_rank"], errors="coerce")
        df["opening_rank"] = pd.to_numeric(df["opening_rank"], errors="coerce")
        df.dropna(subset=["closing_rank", "opening_rank"], inplace=True)
        df["closing_rank"] = df["closing_rank"].astype(int)
        df["opening_rank"] = df["opening_rank"].astype(int)
        df["category"] = category
        combined_data = pd.concat([combined_data, df], ignore_index=True)

    return combined_data
