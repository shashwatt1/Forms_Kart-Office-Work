import streamlit as st
import pandas as pd
from preprocessor import load_data
from helper import filter_data, plot_graphs, convert_df

DEFAULT_BRANCH_PREFERENCE = [
    "Computer Science and Engineering",
    "Electronics and Communication Engineering",
    "Electrical and Electronics Engineering"
]

ALL_23_IITS = [
    "Indian Institute of Technology Bombay", "Indian Institute of Technology Delhi",
    "Indian Institute of Technology Madras", "Indian Institute of Technology Kanpur",
    "Indian Institute of Technology Kharagpur", "Indian Institute of Technology Roorkee",
    "Indian Institute of Technology Guwahati", "Indian Institute of Technology Hyderabad",
    "Indian Institute of Technology Indore", "Indian Institute of Technology (BHU) Varanasi",
    "Indian Institute of Technology Bhubaneswar", "Indian Institute of Technology Gandhinagar",
    "Indian Institute of Technology Jodhpur", "Indian Institute of Technology Patna",
    "Indian Institute of Technology Ropar", "Indian Institute of Technology Mandi",
    "Indian Institute of Technology Palakkad", "Indian Institute of Technology Tirupati",
    "Indian Institute of Technology Dhanbad", "Indian Institute of Technology Bhilai",
    "Indian Institute of Technology Goa", "Indian Institute of Technology Jammu",
    "Indian Institute of Technology Dharwad"
]

def main():
    st.set_page_config(page_title="🎓 JEE Advanced/Main College Predictor", page_icon="📊", layout="wide")
    st.image("Logo.PNG", width=200)

    st.title("🎓 JEE Advanced/Main College Predictor")
    st.write("📊 This tool helps counselors determine possible colleges and branches a student can get based on their JEE rank.")

    with st.spinner("Loading data..."):
        try:
            college_type = st.selectbox(
                "Select College Type:",
                ["Indian Institute of Technology (IIT)", "National Institute of Technology (NIT)", "Indian Institute of Information Technology (IIIT)"]
            )
            data = load_data(college_type)
            data.columns = data.columns.astype(str).str.strip().str.lower()

            col1, col2 = st.columns(2)
            with col1:
                st.metric(label="Total Colleges", value=len(data["institute"].unique()))
            with col2:
                st.metric(label="Total Branches", value=len(data["branch"].unique()))
        except Exception as e:
            st.error(f"Error: {e}")
            return

    st.header("Student Details")
    rank = st.number_input("Enter the student's expected/actual rank:", min_value=1)
    seat_type = st.selectbox("Select the student's seat type:", ["OPEN", "OBC-NCL", "SC", "ST", "EWS"])
    gender = st.selectbox("Select the student's gender:", ["Gender-Neutral", "Female-only (including Supernumerary)"])

    st.subheader("Branch Preferences")
    use_default = st.checkbox("Default Branch Preference Order")
    preferred_branches = [] if use_default else st.multiselect("Select your preferred branches:", options=data["branch"].unique())

    include_5yr = st.checkbox("Include 5-Year Courses")

    if st.button("Show Colleges"):
        if not use_default and not preferred_branches:
            st.warning("Please select the branch preference.")
            return

        filtered_data = filter_data(data, rank, seat_type, gender)

        if use_default:
            default = filtered_data[filtered_data["branch"].isin(DEFAULT_BRANCH_PREFERENCE)]
            default["branch_order"] = default["branch"].apply(lambda x: DEFAULT_BRANCH_PREFERENCE.index(x) if x in DEFAULT_BRANCH_PREFERENCE else len(DEFAULT_BRANCH_PREFERENCE))
            default["institute_order"] = default["institute"].apply(lambda x: ALL_23_IITS.index(x) if x in ALL_23_IITS else len(ALL_23_IITS))
            default = default.sort_values(by=["branch_order", "institute_order"])
            rest = filtered_data[~filtered_data["branch"].isin(DEFAULT_BRANCH_PREFERENCE)].sort_values(by="closing_rank")
            filtered_data = pd.concat([default, rest])
        elif preferred_branches:
            filtered_data = filtered_data[filtered_data["branch"].isin(preferred_branches)]

        if not include_5yr:
            filtered_data = filtered_data[~filtered_data["branch"].str.contains("Dual Degree|Integrated", na=False)]

        if not filtered_data.empty:
            filtered_data["rank_difference"] = abs(filtered_data["closing_rank"] - rank)
            sorted_data = filtered_data.sort_values(by="rank_difference")

            st.subheader(f"🎯 Top 5 Most Likely Options at Rank {rank}:")
            for i in range(min(5, len(sorted_data))):
                entry = sorted_data.iloc[i]
                st.write(f"**College:** {entry['institute']}")
                st.write(f"**Branch:** {entry['branch']}")
                st.write(f"**Opening Rank:** {entry['opening_rank']}")
                st.write(f"**Closing Rank:** {entry['closing_rank']}")
                st.write(f"**Rank Difference:** {entry['rank_difference']}")
                st.markdown("---")

            def highlight_row(row):
                return ["background-color: lightgreen" if abs(row["closing_rank"] - rank) <= 50 else ""] * len(row)

            st.subheader("Filtered Colleges and Branches")
            st.dataframe(sorted_data.style.apply(highlight_row, axis=1))

            csv = convert_df(sorted_data)
            st.download_button("📥 Download Filtered Data as CSV", data=csv, file_name="filtered_colleges.csv", mime="text/csv")

            st.subheader("Visualization")
            bar, pie = plot_graphs(sorted_data)
            st.plotly_chart(bar, use_container_width=True)
            st.plotly_chart(pie, use_container_width=True)
        else:
            st.warning("Sorry! No data found for the given rank, seat type, and gender. Try different inputs.")

    st.markdown("---")
    st.markdown("Developed by **[Shashwat Malviya](https://www.linkedin.com/in/shashwatt1/)**")

if __name__ == "__main__":
    main()
