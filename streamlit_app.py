import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Gym Member Analysis", layout="wide")

st.title("Gym Members Exercise Tracking Analysis")

df = pd.read_csv("gym_members_exercise_tracking_synthetic_data.csv")

st.header("Dataset")
st.write("The first few rows of the dataset:")
st.dataframe(df.head())

st.header("Basic Statistics")
st.write(df.describe())
st.write("Count line shows us number of non-NA/null observations. We have 1800 rows in each column. Each column have nan values.")

st.header("Missing Values")
st.write("Number of missing values in each column:")
st.write(df.isna().sum())
st.write("isna function show number of nan values in each column, which proves that dataset has nan fields.")

st.write(df.info())
st.write("We can observe that besides 'Gender' and 'Workout_Type' which are obvious are not numerical columns there is a 'Max_BPM' column with Object data type included")

st.header("Cleaning")
st.write("Change of data type in the Max_BPM column")
df['Max_BPM'] = pd.to_numeric(df['Max_BPM'], errors='coerce')
st.write(df.info())

st.write("We can not fillin columns 'Gender' and 'Workout_Type' with average values. So I prefer to drop out lines with blank fields in this columns.")
st.write("I think in real world age is super important for fitness data. So I decided not to fill it with average and delete lines with nans.")
df = df.dropna(subset=['Age', 'Gender', 'Workout_Type'])
st.write(df.isna().sum())

st.write("If we delete all the lines with nans we will lose about 1/3 of dataset. Therefore I decided to fillin fileds with average values for each column.")
columns_to_fill = [
    "Avg_BPM", "Max_BPM", "Weight (kg)", "Height (m)", "Resting_BPM",
    "Session_Duration (hours)", "Calories_Burned", "Fat_Percentage",
    "Water_Intake (liters)", "Workout_Frequency (days/week)", "Experience_Level", "BMI"
]

for col in columns_to_fill:
    mean_value = df[col].mean()
    df[col] = df[col].fillna(mean_value)

valid_workout_types = ["Strength", "Cardio", "HIIT", "Yoga"]
df.loc[~df['Workout_Type'].isin(valid_workout_types), 'Workout_Type'] = None
df = df.dropna(subset=['Workout_Type']).reset_index(drop=True)
st.write(df.isna().sum())

st.header("Histograms")
st.write("Distribution of numerical columns:")
fig, ax = plt.subplots(figsize=(16, 12))
df.hist(bins=20, ax=ax)
st.pyplot(fig)

st.header("Gender Distribution")
fig = px.pie(df, names="Gender", title="Gender Distribution")
st.plotly_chart(fig)

st.header("Workout Type Distribution")
fig = px.bar(df, x='Workout_Type', color="Workout_Type", title='Workout Type Distribution')
st.plotly_chart(fig)

st.header("Correlation Heatmap")
fig, ax = plt.subplots(figsize=(15, 10))
sns.heatmap(df.corr(numeric_only=True), annot=True, cmap="Greys", ax=ax)
plt.title('Correlation')
st.pyplot(fig)

st.header("Average BPM by Age")
fig = px.scatter(df, y='Avg_BPM', x='Age', title='Average BPM in Different Ages')
st.plotly_chart(fig)

st.header("Height and Weight by Gender")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Height Distribution by Gender")
    fig = px.histogram(df, x="Height (m)", color="Gender", title="Height Distribution by Gender")
    st.plotly_chart(fig)

with col2:
    st.subheader("Weight Distribution by Gender")
    fig = px.histogram(df, x="Weight (kg)", color="Gender", title="Weight Distribution by Gender")
    st.plotly_chart(fig)
    
st.header("Calories Burned by Workout Type (Cardio & HIIT)")
fig = px.scatter(df[df['Workout_Type'].isin(['Cardio', 'HIIT'])], x='Session_Duration (hours)', y='Calories_Burned', 
    color='Workout_Type', facet_col='Workout_Type',
    title="Calories Burned by Session Duration for Cardio & HIIT"
)
st.plotly_chart(fig)


