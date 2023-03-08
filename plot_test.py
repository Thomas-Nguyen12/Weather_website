import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
sns.set()
df = pd.read_csv("greenhouse.csv")
Australia = df[df.country_or_area == "Australia"]
australia = Australia.groupby(["year"])["value"].mean()
australia = pd.DataFrame(australia)
australia["year"] = [i for i in australia.index]
fig, ax = plt.subplots()
ax.plot(australia.year, australia.value)
ax.set_xlabel("year")
ax.set_ylabel("mean_value")
import streamlit as st
with st.container():
    st.pyplot(fig)