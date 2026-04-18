import pandas as pd

# Loading the dataset
df = pd.read_csv(r'C:\Users\KIIT\OneDrive\Desktop\project\python with machine learning project\dataset\original_data.csv\indian_colleges.csv')

# Cleaning column names
df.columns = df.columns.str.strip().str.lower()

# Function to recommend colleges
def recommend_colleges(rank, budget, course, location=None):
    
    # Filtering the data
    filtered = df[
        (df['course'].str.lower() == course.lower()) &
        (df['cutoff_rank'] >= rank) &
        (df['fees'] <= budget)
    ]
    
    if location:
        filtered = filtered[filtered['location'].str.lower() == location.lower()]
    
    if filtered.empty:
        return "No colleges found. Try relaxing filters."
    
    # Scoring logic
    filtered['score'] = (
        (1 / filtered['cutoff_rank']) * 0.4 +
        (filtered['placement_percent'] / 100) * 0.3 +
        (filtered['avg_package_lpa'] / 20) * 0.3
    )
    
    
    result = filtered.sort_values(by='score', ascending=False)
    
    return result[['college', 'course', 'location', 'fees', 'placement_percent', 'avg_package_lpa']].head(5)


result = recommend_colleges(
    rank=100,
    budget=200000,
    course="CSE",
    location="delhi"
)

print(result)