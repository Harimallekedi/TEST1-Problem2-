import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
@st.cache
def load_data():
    data = pd.read_csv('university_student_dashboard_data.csv')
    return data

data = load_data()

# Set up the Streamlit app
st.title('University Student Dashboard')
st.sidebar.header('Filters')

# Sidebar filters
selected_year = st.sidebar.selectbox('Select Year', data['Year'].unique())
selected_term = st.sidebar.selectbox('Select Term', data['Term'].unique())

# Filter data based on selections
filtered_data = data[(data['Year'] == selected_year) & (data['Term'] == selected_term)]

# Display key metrics
st.header('Key Metrics')
col1, col2, col3 = st.columns(3)
col1.metric("Total Applications", filtered_data['Applications'].values[0])
col2.metric("Total Admissions", filtered_data['Admitted'].values[0])
col3.metric("Total Enrollments", filtered_data['Enrolled'].values[0])

# Retention Rate Trends
st.header('Retention Rate Trends Over Time')
retention_data = data.groupby('Year')['Retention Rate (%)'].mean().reset_index()
fig, ax = plt.subplots()
sns.lineplot(data=retention_data, x='Year', y='Retention Rate (%)', ax=ax)
st.pyplot(fig)

# Student Satisfaction Trends
st.header('Student Satisfaction Trends Over Time')
satisfaction_data = data.groupby('Year')['Student Satisfaction (%)'].mean().reset_index()
fig, ax = plt.subplots()
sns.lineplot(data=satisfaction_data, x='Year', y='Student Satisfaction (%)', ax=ax)
st.pyplot(fig)

# Enrollment Breakdown by Department
st.header('Enrollment Breakdown by Department')
department_data = filtered_data[['Engineering Enrolled', 'Business Enrolled', 'Arts Enrolled', 'Science Enrolled']]
st.bar_chart(department_data.T)

# Comparison between Spring and Fall terms
st.header('Spring vs. Fall Term Trends')
term_comparison = data.groupby(['Year', 'Term']).agg({
    'Applications': 'mean',
    'Admitted': 'mean',
    'Enrolled': 'mean',
    'Retention Rate (%)': 'mean',
    'Student Satisfaction (%)': 'mean'
}).reset_index()
fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(data=term_comparison, x='Year', y='Enrolled', hue='Term', ax=ax)
st.pyplot(fig)

# Key Findings and Insights
st.header('Key Findings and Insights')
st.write("""
- **Retention Rate**: The retention rate has shown a steady increase over the years, indicating improved student support and engagement.
- **Student Satisfaction**: Student satisfaction scores have also increased, reflecting positive changes in the academic environment.
- **Enrollment Trends**: Engineering and Business departments have seen consistent growth in enrollments, while Arts and Science have remained relatively stable.
- **Term Comparison**: Fall terms generally have slightly higher enrollments compared to Spring terms.
""")

# Run the app
if __name__ == '__main__':
    st.run()
