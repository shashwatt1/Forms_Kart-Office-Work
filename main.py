import streamlit as st
import pandas as pd  # Add this import for pandas
from preprocessor import load_data
from helper import filter_data, plot_graphs, convert_df

# Define the default branch preference order
DEFAULT_BRANCH_PREFERENCE = [
    "Computer Science and Engineering",
    "Electronics and Communication Engineering",
    "Electrical and Electronics Engineering"
]

# Define the top 7 IITs (placeholder - update with the actual order)
TOP_7_IITS = [
    "Indian Institute of Technology Bombay",
    "Indian Institute of Technology Delhi",
    "Indian Institute of Technology Madras",
    "Indian Institute of Technology Kanpur",
    "Indian Institute of Technology Kharagpur",
    "Indian Institute of Technology Roorkee",
    "Indian Institute of Technology Guwahati"
]

# Define all 23 IITs (placeholder - update with the actual order)
ALL_23_IITS = [
    "Indian Institute of Technology Bombay",
    "Indian Institute of Technology Delhi",
    "Indian Institute of Technology Madras",
    "Indian Institute of Technology Kanpur",
    "Indian Institute of Technology Kharagpur",
    "Indian Institute of Technology Roorkee",
    "Indian Institute of Technology Guwahati",
    "Indian Institute of Technology Hyderabad",
    "Indian Institute of Technology Indore",
    "Indian Institute of Technology (BHU) Varanasi",
    "Indian Institute of Technology Bhubaneswar",
    "Indian Institute of Technology Gandhinagar",
    "Indian Institute of Technology Jodhpur",
    "Indian Institute of Technology Patna",
    "Indian Institute of Technology Ropar",
    "Indian Institute of Technology Mandi",
    "Indian Institute of Technology Palakkad",
    "Indian Institute of Technology Tirupati",
    "Indian Institute of Technology Dhanbad",
    "Indian Institute of Technology Bhilai",
    "Indian Institute of Technology Goa",
    "Indian Institute of Technology Jammu",
    "Indian Institute of Technology Dharwad"
]

# Main App
def main():
    # Set page config
    st.set_page_config(
        page_title="🎓 JEE Advanced/Main College Predictor",
        page_icon="📊",
        layout="wide"
    )

    # Add a logo
    st.image("Logo.PNG", width=200)

    # Title and description
    st.title("🎓 JEE Advanced/Main College Predictor")
    st.write("📊 This tool helps counselors determine possible colleges and branches a student can get based on their JEE rank.")

    # Load the data with a spinner
    with st.spinner("Loading data..."):
        try:
            # Input field for college type
            college_type = st.selectbox(
                "Select College Type:",
                ["Indian Institute of Technology (IIT)", "National Institute of Technology (NIT)", "Indian Institute of Information Technology (IIIT)" ],
                help="Choose the type of college you want to predict for."
            )

           
           # Load data based on college type
            if college_type == "Indian Institute of Technology (IIT)":
            data = load_data("IIT")
            elif college_type == "National Institute of Technology (NIT)":
            data = load_data("NIT")
            elif college_type == "Indian Institute of Information Technology (IIIT)":
            data = load_data("IIIT")


            # Remove the "Data loaded successfully!" prompt
            # st.success(f"Data loaded successfully! Total entries: {len(data)}")

            # Display summary metrics in columns
            col1, col2 = st.columns(2)
            with col1:
                st.metric(label="Total Colleges", value=len(data["institute"].unique()))
            with col2:
                st.metric(label="Total Branches", value=len(data["branch"].unique()))

        except FileNotFoundError as e:
            st.error(f"Error: {e}")
            return

    # Input fields for student details
    st.header("Student Details")
    rank = st.number_input(
        "Enter the student's expected/actual rank:", 
        min_value=1, 
        help="Rank based on JEE Advanced/Main results."
    )
    seat_type = st.selectbox(
        "Select the student's seat type:",
        ["OPEN", "OBC-NCL", "SC", "ST", "EWS"],
        help="Choose the applicable category."
    )
    gender = st.selectbox(
        "Select the student's gender:",
        ["Gender-Neutral", "Female-only (including Supernumerary)"],
        help="Gender-specific seats available."
    )

    # Branch preference filter
    st.subheader("Branch Preferences")
    use_default_branch_preference = st.checkbox(
        "Default Branch Preference Order",
        help="Check this box to use the default branch preference order (CSE, ECE, EEE for IITs)."
    )

    if not use_default_branch_preference:
        preferred_branches = st.multiselect(
            "Select your preferred branches:",
            options=data["branch"].unique(),
            help="Choose the branches you are interested in."
        )
    else:
        preferred_branches = []

    # 5-Year course filter
    include_5_year_courses = st.checkbox(
        "Include 5-Year Courses",
        help="Check this box to include 5-year courses (e.g., Dual Degree programs)."
    )

    if st.button("Show Colleges"):
        # Check if branch preferences are selected
        if not use_default_branch_preference and not preferred_branches:
            st.warning("Please select the branch preference.")
            return

        # Filter data based on rank, seat type, and gender
        filtered_data = filter_data(data, rank, seat_type, gender)

        # Apply branch preference filter
        if use_default_branch_preference:
            # Apply default branch preference order
            default_branches_data = filtered_data[filtered_data["branch"].isin(DEFAULT_BRANCH_PREFERENCE)]
            # Sort by default branch preference and IIT order
            default_branches_data["branch_order"] = default_branches_data["branch"].apply(
                lambda x: DEFAULT_BRANCH_PREFERENCE.index(x) if x in DEFAULT_BRANCH_PREFERENCE else len(DEFAULT_BRANCH_PREFERENCE)
            )
            default_branches_data["institute_order"] = default_branches_data["institute"].apply(
                lambda x: ALL_23_IITS.index(x) if x in ALL_23_IITS else len(ALL_23_IITS)
            )
            default_branches_data = default_branches_data.sort_values(by=["branch_order", "institute_order"])

            # Get remaining branches (not in default preference)
            remaining_branches_data = filtered_data[~filtered_data["branch"].isin(DEFAULT_BRANCH_PREFERENCE)]
            # Sort remaining branches by closing rank
            remaining_branches_data = remaining_branches_data.sort_values(by="closing_rank")

            # Combine default and remaining branches
            filtered_data = pd.concat([default_branches_data, remaining_branches_data])
        elif preferred_branches:
            # Apply user-selected branch preferences
            filtered_data = filtered_data[filtered_data["branch"].isin(preferred_branches)]

        # Apply 5-Year course filter
        if not include_5_year_courses:
            # Exclude 5-year courses (assuming they contain "Dual Degree" or "Integrated" in the branch name)
            filtered_data = filtered_data[~filtered_data["branch"].str.contains("Dual Degree|Integrated")]

        if not filtered_data.empty:
            # Calculate the absolute difference between the input rank and closing rank
            filtered_data["rank_difference"] = abs(filtered_data["closing_rank"] - rank)

            # Sort the data by rank difference to find the closest matches
            sorted_data = filtered_data.sort_values(by="rank_difference")

            # Display the top 5 closest matches
            st.subheader(f"🎯 Top 5 Most Likely Options at Rank {rank}:")
            for i in range(min(5, len(sorted_data))):  # Show up to 5 options
                college = sorted_data.iloc[i]["institute"]
                branch = sorted_data.iloc[i]["branch"]
                opening_rank = sorted_data.iloc[i]["opening_rank"]
                closing_rank = sorted_data.iloc[i]["closing_rank"]
                rank_diff = sorted_data.iloc[i]["rank_difference"]

                st.write(f"**College:** {college}")
                st.write(f"**Branch:** {branch}")
                st.write(f"**Opening Rank:** {opening_rank}")
                st.write(f"**Closing Rank:** {closing_rank}")
                st.write(f"**Rank Difference:** {rank_diff}")
                st.markdown("---")  # Add a separator between options

            # Highlight rows where closing rank is within ±50 of the student's rank
            def highlight_row(row):
                if abs(row["closing_rank"] - rank) <= 50:
                    return ["background-color: lightgreen"] * len(row)
                else:
                    return [""] * len(row)

            # Apply the highlight function to the DataFrame
            highlighted_data = sorted_data.style.apply(highlight_row, axis=1)

            # Display filtered results
            st.subheader("Filtered Colleges and Branches")
            st.dataframe(highlighted_data)

            # Download option
            csv = convert_df(sorted_data)
            st.download_button(
                label="📥 Download Filtered Data as CSV",
                data=csv,
                file_name="filtered_colleges.csv",
                mime="text/csv",
            )

            # Plot graphs
            st.subheader("Visualization")
            bar_chart, pie_chart = plot_graphs(sorted_data)
            st.plotly_chart(bar_chart, use_container_width=True)
            st.plotly_chart(pie_chart, use_container_width=True)

        else:
            # Show a pop-up message if no data is found
            st.warning("Sorry! No data found for the given rank, seat type, and gender. Try different inputs.")

    # Footer
    st.markdown("---")
    st.markdown("Developed by **[Shashwat Malviya](https://www.linkedin.com/in/shashwatt1/)**")

if __name__ == "__main__":
    main()
