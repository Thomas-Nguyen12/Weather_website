import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np

sns.set()
df = pd.read_csv("greenhouse.csv")
Australia = df[df.country_or_area == "Australia"]
australia = Australia.groupby(["year"])["value"].mean()
australia = pd.DataFrame(australia)
australia["year"] = [i for i in australia.index]
australia.index = [i for i in range(len(australia))]
fig, ax = plt.subplots()
reg = np.polyfit(australia.year, australia.value, deg=1)
trend = np.polyval(reg, australia.year)

ax.plot(australia.year, australia.value)
ax.plot(australia.year, trend)
ax.set_xlabel("year")
ax.set_ylabel("mean_value")
ax.legend(["observed data", "line of best fit"])



import streamlit as st
with st.container():
    st.pyplot(fig)
with st.container():
    st.line_chart(data=australia, x="year", y="value")
st.dataframe(australia)