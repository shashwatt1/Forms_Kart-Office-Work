import pandas as pd
import plotly.express as px

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
    
    # Apply default branch filter if enabled
    if default_preference:
        college_type = 'IIT' if 'Indian Institute of Technology' in filtered['institute'].iloc[0] else 'NIT'
        filtered = filtered[filtered['branch'].isin(DEFAULT_BRANCHES[college_type])]
    
    # Exclude 5-year courses if enabled
    if exclude_five_year:
        filtered = filtered[~filtered['branch'].str.contains('Dual Degree|Integrated|5 Year')]
    
    # Apply branch preference filter if specified
    if branch_preference:
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
