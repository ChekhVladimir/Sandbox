import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import io

code = """
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
"""
st.code(code, language='python')

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

buffer = io.StringIO()
df.info(buf=buffer)
s = buffer.getvalue()
st.code(s)
st.write("We can observe that besides 'Gender' and 'Workout_Type' which are obvious are not numerical columns there is a 'Max_BPM' column with Object data type included")



st.header("Cleaning")
st.write("Change of data type in the Max_BPM column")
df['Max_BPM'] = pd.to_numeric(df['Max_BPM'], errors='coerce')

buffer = io.StringIO()
df.info(buf=buffer)
s = buffer.getvalue()
st.code(s)

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

st.header("Workout fields check")
fig = px.bar(df, x = 'Workout_Type', color = 'Workout_Type', title = 'Workout types')
st.plotly_chart(fig)
st.write("As we can see there is some data that matches with other categories but changed a bit, so I will delete all the other types of Workout besides Strength, Cardio, HIIT and Yoga.")

valid_workout_types = ["Strength", "Cardio", "HIIT", "Yoga"]
df.loc[~df['Workout_Type'].isin(valid_workout_types), 'Workout_Type'] = None
df = df.dropna(subset=['Workout_Type']).reset_index(drop=True)
st.write(df.isna().sum())



st.header("Overview")
st.write("Distribution of numerical columns:")
fig, ax = plt.subplots(figsize=(16, 12))
df.hist(bins=20, ax=ax)
st.pyplot(fig)
st.write("We can see that there is no zero values in data.")

fig = px.pie(df, names="Gender", title="Gender Distribution")
st.plotly_chart(fig)

fig = px.bar(df, x='Workout_Type', color="Workout_Type", title='Workout Type Distribution')
st.plotly_chart(fig)

st.header("Correlation Heatmap")
fig, ax = plt.subplots(figsize=(15, 10))
sns.heatmap(df.corr(numeric_only=True), annot=True, cmap="Greys", ax=ax)
plt.title('Correlation')
st.pyplot(fig)
st.write("We can observe that there is no any correlation between two colomns. Most likely that means that dataset is synthetic and values in each colomn were generated independently.")



st.header("More Detailed Overview")
fig = px.scatter(df, y='Avg_BPM', x='Age', title='Average BPM in Different Ages')
st.plotly_chart(fig)
st.write("Average BPM is not depended on age.")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Height Distribution by Gender")
    fig = px.histogram(df, x="Height (m)", color="Gender", title="Height Distribution by Gender")
    st.plotly_chart(fig)

with col2:
    st.subheader("Weight Distribution by Gender")
    fig = px.histogram(df, x="Weight (kg)", color="Gender", title="Weight Distribution by Gender")
    st.plotly_chart(fig)
st.write("Height and Weight distribution completly independent from gender in this dataset.")

st.write("Let's see if the number of calories burned depends on the duration of the workout for Cardio and HIIT.")
fig = px.scatter(df[df['Workout_Type'].isin(['Cardio', 'HIIT'])], x='Session_Duration (hours)', y='Calories_Burned', 
    color='Workout_Type', facet_col='Workout_Type',
    title="Calories Burned by Session Duration for Cardio & HIIT"
)
st.plotly_chart(fig)
st.write("We can see that calories burned is not depended on session duration for cardio and HIIT workouts.")

fig = px.box(df, x="Workout_Type", y="Session_Duration (hours)", title="Session duration depended on Workout type")
st.plotly_chart(fig)
st.write("We do not see significant difference in session duration for different workout types.")

fig = px.scatter(df.loc[df['Experience_Level'] == 3], y ='Water_Intake (liters)', x ='Fat_Percentage', color = 'Session_Duration (hours)',title='Water Intake affecting on Fat Percentage')
st.plotly_chart(fig)
st.write("This graph shows dependence of water inteka to fat percentage for people with experience level 3 for different session duration.")
st.write("We can observe that there is no correlation between fat percentage and water intake.")

avg_bpm_df = df.groupby("Workout_Type", as_index=False)["Avg_BPM"].mean()
fig = px.bar(avg_bpm_df, x="Workout_Type", y="Avg_BPM",
             title="Average BPM during different workouts", color="Workout_Type")
st.plotly_chart(fig)
st.write("It is clearly seen that therre is almost no difference between workouts in BPM.")

st.header("Hypothesis checking")
st.write("Dataset is randomly generated and each column filled independently.")
st.header("Prove")
st.write("BMI index is equal to weight divided by squared height.")
st.write("Let's create a new column called Calculated_BMI.")
st.header("Data Transformation 1")
st.write("Calculating BMI index according to formula: ")
st.latex(r"""{BMI} = \frac{\text{Weight}}{\text{Height}^2}""")
df['Calculated_BMI'] = (df['Weight (kg)'] / (df['Height (m)'] ** 2))
subset = ['BMI', 'Calculated_BMI', 'Weight (kg)', 'Height (m)']
st.dataframe(df[subset])

fig, ax = plt.subplots(figsize=(5, 3))
subset = ['BMI', 'Calculated_BMI', 'Weight (kg)', 'Height (m)']
sns.heatmap(df[subset].corr(numeric_only=True), annot=True, cmap="Greys", ax=ax)
plt.title('Correlation')
st.pyplot(fig)
st.write("Calculated_BMI is highly dependent on Weight and Height.")
st.write("BMI in dataset is not depended on Weight and Height.")
st.write("There is no dependency between BMI and Calculated_BMI.")

fig = px.scatter(df, x = 'Weight (kg)', y = 'Calculated_BMI', color = 'Height (m)')
st.plotly_chart(fig)

fig = px.scatter(df, x = 'Weight (kg)', y = 'BMI', color = 'Height (m)')
st.plotly_chart(fig)
st.write("We see that Calculated_BMI is depended on Weight and Height.")
st.write("BMI from dataset is completly independend.")

st.header("Data Transformation 2")
st.write("Calculating if Avg_BPM is bigger than Max_BPM. It is contradicting situation.")
st.latex(r"""{Check  BPM} = \text{Max BPM} - \text{Avg BPM}""")

df['Check_BPM'] = (df['Max_BPM'] - df['Avg_BPM'] > 0)
subset = ['Check_BPM', 'Max_BPM', 'Avg_BPM']
st.dataframe(df[subset])

fig = px.scatter(df.loc[df['Workout_Type'] == 'Strength'], x = 'Avg_BPM', y = 'Max_BPM', color = 'Check_BPM' ,title = 'BPM depended on workout type')
st.plotly_chart(fig)
st.write("Another prove that dataset is generated randomly and columns are independent. On this graph we see Max_BPM and Avg_BPM. We see that where is no dependency bethween this two columns. Moreover, there are cases when Average BPM is higher than Maximum BPM which is not realistic.")

buffer = io.StringIO()
df.info(buf=buffer)
s = buffer.getvalue()
st.code(s)

st.header("Conclusion")
st.write("Dataset is interesting for data cleaning and wide variety of different columns. Unfortunatly it is randomly generated and it is not possible to use this data for conclusions. ")
