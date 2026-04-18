import streamlit as st
import pandas as pd

# Load dataset
df = pd.read_csv(r'C:\Users\KIIT\OneDrive\Desktop\project\python with machine learning project\dataset\original_data.csv\indian_colleges.csv')
df.columns = df.columns.str.strip().str.lower()

st.title("Indian College Recommendation System")

# Inputs
rank = st.number_input("Enter Rank", min_value=1, value=10000)
budget = st.number_input("Enter Budget", min_value=10000, value=200000)

course = st.selectbox("Select Course", df['course'].unique())
location = st.selectbox("Select Location", ["Any"] + list(df['location'].unique()))

if st.button("Get Recommendations"):
    
    filtered = df[
        (df['course'] == course) &
        (df['cutoff_rank'] >= rank) &
        (df['fees'] <= budget)
    ]
    
    if location != "Any":
        filtered = filtered[filtered['location'] == location]
    
    if filtered.empty:
        st.warning("No colleges found. Try different inputs.")
    else:
        filtered['score'] = (
            (1 / filtered['cutoff_rank']) * 0.4 +
            (filtered['placement_percent'] / 100) * 0.3 +
            (filtered['avg_package_lpa'] / 20) * 0.3
        )
        
        result = filtered.sort_values(by='score', ascending=False).head(5)
        
        st.subheader("Top Recommended Colleges")
        st.dataframe(result[['college','course','location','fees','placement_percent','avg_package_lpa']])