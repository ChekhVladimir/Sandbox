import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px

st.write('Hello World!')

df = pd.read_csv("gym_members_exercise_tracking_synthetic_data.csv")
st.dataframe(df)

st.dataframe(df.describe())

st.dataframe(df.isna().sum())

df['Max_BPM'] = pd.to_numeric(df['Max_BPM'], errors='coerce')
df.info()
