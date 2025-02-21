import streamlit as st
from helper import load_data, filter_data  # Import helper functions

# Streamlit layout
def main():
    st.title("JEE Advanced/Main College Predictor")
    st.write("This tool helps counselors determine the possible colleges and branches a student can get based on their JEE rank.")

    # Load the data (no need to show the raw data anymore)
    try:
        data = load_data()
        st.success("Data loaded and cleaned successfully!")

        # Input fields for student details
        st.header("Student Details")
        rank = st.number_input("Enter the student's expected/actual rank:", min_value=1)
        seat_type = st.selectbox("Select the student's seat type:", ["Home State", "Other State"])  # Seat Type instead of Category
        gender = st.selectbox("Select the student's gender:", ["Male", "Female", "Other"])

        if st.button("Predict Colleges"):
            # Filter data using the helper function
            filtered_data = filter_data(data, rank, seat_type, gender)
            
            if not filtered_data.empty:
                st.success(f"Found {len(filtered_data)} options for the given rank, seat type, and gender!")
                
                # Display filtered results
                st.subheader("Filtered Colleges and Branches")
                st.dataframe(filtered_data)  # Display in a table format
            else:
                st.warning("No options found for the given rank, seat type, and gender. Please try different inputs.")
    except ValueError as e:
        st.error(f"Error: {e}")

if __name__ == "__main__":
    main()
