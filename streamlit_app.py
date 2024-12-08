import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns

st.write('Hello World!')

df = pd.read_csv("gym_members_exercise_tracking_synthetic_data.csv")
st.dataframe(df)

st.dataframe(df.describe())

st.dataframe(df.isna().sum())

st.dataframe(df.info())

