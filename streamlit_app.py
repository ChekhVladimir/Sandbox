import numpy as np
import pandas as pd
import plotly.express as px
import seaborn as sns
import streamlit as st

st.write('Hello World!')

df = pd.read_csv("gym_members_exercise_tracking_synthetic_data.csv")
st.write(df)
