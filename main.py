import streamlit as st
from preprocessor import load_data
from helper import filter_data, plot_graphs, convert_df

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
    st.write("This tool provides students with insights into the most probable colleges they can secure admission to based on the previous year's cutoff trends.")
    st.write("Data Source: JOSAA")

    # Load the data with a spinner
    with st.spinner("Loading data..."):
        try:
            # Input field for college type
            college_type = st.selectbox(
                "Select College Type:",
                ["Indian Institute of Technology (IIT)", "National Institute of Technology (NIT)"],
                help="Choose the type of college you want to predict for."
            )

            # Load data based on college type
            if college_type == "Indian Institute of Technology (IIT)":
                data = load_data("IIT")
            else:
                data = load_data("NIT")

            total_entries = len(data)
            
        except FileNotFoundError as e:
            st.error(f"Error: {e}")
            return

    # Display summary metrics in columns
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Total Colleges", value=len(data["institute"].unique()))
    with col2:
        st.metric(label="Total Branches", value=len(data["branch"].unique()))

    # Input fields for student details
    st.header("Student Details")
    rank = st.number_input(
        "Enter the student's expected/actual rank:", 
          min_value= 1, 
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

    if st.button("Show Colleges"):
        # Filter data
        filtered_data = filter_data(data, rank, seat_type, gender)

        if not filtered_data.empty:
            # Calculate the absolute difference between the input rank and closing rank
            filtered_data["rank_difference"] = abs(filtered_data["closing_rank"] - rank)

            # Sort the data by rank difference to find the closest match
            sorted_data = filtered_data.sort_values(by="rank_difference")

            # Display the most likely college and branch (closest match)
            most_likely_college = sorted_data.iloc[0]["institute"]
            most_likely_branch = sorted_data.iloc[0]["branch"]
            st.subheader(f"Most Likely Option at Rank {rank}:")
            st.write(f"**🏫 College:** {most_likely_college}")
            st.write(f"**📚 Branch:** {most_likely_branch}")

            # Highlight rows where closing rank is within ±50 of the student's rank
            def highlight_row(row):
                if abs(row["closing_rank"] - rank) <= 50:
                    return ["background-color: lightgreen"] * len(row)
                else:
                    return [""] * len(row)

            # Apply the highlight function to the DataFrame
            highlighted_data = sorted_data.style.apply(highlight_row, axis=1)

            # Display filtered results
            st.subheader("📋 Filtered Colleges and Branches")
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
            st.subheader("📊 Visualization")
            bar_chart, pie_chart = plot_graphs(sorted_data)
            st.plotly_chart(bar_chart, use_container_width=True)
            st.plotly_chart(pie_chart, use_container_width=True)

        else:
            # Show a pop-up message if no data is found
            st.warning("Sorry! No data found for the given rank, seat type, and gender. Try different inputs.")

    # Footer
    st.markdown("---")
    st.markdown("Developed by **[Shashwat Malviya and Team Forms_Kart](https://www.linkedin.com/in/shashwatt1/)**")

if __name__ == "__main__":
    main()
