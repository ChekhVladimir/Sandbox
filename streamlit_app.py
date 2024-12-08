import numpy as np
import pandas as pd
import streamlit as st

st.write('Hello World!')

df = pd.read_csv("gym_members_exercise_tracking_synthetic_data.csv")
st.dataframe(df)
