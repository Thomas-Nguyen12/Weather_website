from bokeh.plotting import figure
from bokeh.palettes import inferno
import plotly.graph_objects as go
import pandas as pd 
from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
emission = pd.read_csv("greenhouse.csv")
emission["text"] = "Location: " + emission["country"]

unique = emission.country.unique()
fig = go.Figure(data=go.Choropleth(
    locations=emission["text"],
    z=emission["value"].astype(float),
    locationmode="country names",
    colorscale="thermal",
    colorbar_title="emission",
    text=emission["text"] # Hover text
))

fig.update_layout(
    title_text="Greenhouse emission",
    geo_scope="world",
    
)