import pandas as pd
import plotly.express as px

# Helper Function: Filter Data
def filter_data(data, rank, seat_type, gender):
    """
    Filters the data based on rank, seat type, and gender.
    Returns a filtered DataFrame.
    """
    filtered = data[
        (data["closing_rank"] >= rank) &  # Filter by closing rank greater than or equal to student's rank
        (data["seat_type"] == seat_type) &  # Filter by selected seat type
        (data["gender"] == gender)  # Filter by selected gender
    ]

    # Highlight rows where closing rank is within ± 100 of the student's rank
    filtered["highlight"] = filtered["closing_rank"].apply(lambda x: "lightgreen" if abs(x - rank) <= 100 else "")
    
    return filtered

# Helper Function: Convert DataFrame to CSV for Download
def convert_df(df):
    """Converts a DataFrame to CSV for download."""
    return df.to_csv(index=False).encode('utf-8')

# Helper Function: Plot Graphs
def plot_graphs(filtered_data):
    """
    Generates and saves interactive visualizations for filtered data.
    """
    # Bar chart: Number of branches per institute
    bar_chart = px.bar(
        filtered_data.groupby("institute")["branch"].count().reset_index(),
        x="institute",
        y="branch",
        title="Number of Branches per Institute",
        labels={"branch": "Number of Branches", "institute": "Institute"},
        color="branch",
        color_continuous_scale="Viridis"
    )

    # Pie chart: Percentage of institutes offering branches
    pie_chart = px.pie(
        filtered_data,
        names="institute",
        title="Chances of Getting Colleges",
        hole=0.4
    )

    return bar_chart, pie_chart