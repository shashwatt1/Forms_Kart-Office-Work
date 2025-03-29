import pandas as pd
import plotly.express as px
import re

# Default branches for filtering
DEFAULT_BRANCHES = {
    'IIT': ['Computer Science and Engineering', 'Electrical Engineering', 
            'Mechanical Engineering', 'Electronics and Communication Engineering',
            'Chemical Engineering', 'Civil Engineering'],
    'NIT': ['Computer Science and Engineering', 'Electrical Engineering',
            'Electronics and Communication Engineering', 'Mechanical Engineering',
            'Civil Engineering', 'Information Technology']
}

def filter_data(data, rank, seat_type, gender, default_preference=True, 
                exclude_five_year=True, branch_preference=None):
    """
    Filters the data based on multiple criteria.
    """
    # Basic filtering
    filtered = data[
        (data["closing_rank"] >= rank) &
        (data["seat_type"] == seat_type) &
        (data["gender"] == gender)
    ].copy()
    
    # Debug info for empty results
    if filtered.empty:
        print(f"Debug - Available seat types in data: {data['seat_type'].unique()}")
        print(f"Debug - Available genders in data: {data['gender'].unique()}")
        print(f"Debug - Requested filters - Seat: {seat_type}, Gender: {gender}, Rank: {rank}")
    
    # Apply default branch filter if enabled
    if default_preference and not filtered.empty:
        college_type = 'IIT' if 'Indian Institute of Technology' in str(filtered['institute'].iloc[0]) else 'NIT'
        filtered = filtered[filtered['branch'].isin(DEFAULT_BRANCHES[college_type])]
    
    # Enhanced 5-year course filtering
    if exclude_five_year and not filtered.empty:
        five_year_keywords = [
            'dual', 'integrated', '5 year', '5-year', 'b\.tech\.', 
            'm\.tech\.', 'm\.sc\.', 'dual degree', 'double degree'
        ]
        pattern = '|'.join(five_year_keywords)
        filtered = filtered[~filtered['branch'].str.lower().str.contains(pattern)]
    
    # Apply branch preference filter if specified
    if branch_preference and not filtered.empty:
        filtered = filtered[filtered['branch'].isin(branch_preference)]
    
    return filtered

def convert_df(df):
    """Converts a DataFrame to CSV for download."""
    return df.to_csv(index=False).encode('utf-8')

def plot_graphs(filtered_data):
    """
    Generates visualizations for filtered data.
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
