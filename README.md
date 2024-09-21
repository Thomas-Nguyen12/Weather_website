# New Eltham Weather and greenhouse emission monitoring 

## Project Description 
Global warming is a problem that causes frequent and intense droughts, storms, heat waves, rising sea levels, melting glaciers and warming oceans. 
The global mean near-surface temperature for each year between 2024 and 2028 is predicted to be between 1.1°C and 1.9°C higher than the 1850-1900 baseline, 
according to the WMO report (Harboure, 2024).

This project aims to analyse weather patterns in New Eltham alongside Global Greenhouse emissions. To do this, I have fitted a Random Forecast Classifier model to 
classify countries with certain emissions and regions. In the future, I plan on tracking historical temperature variations to forecast future ones 
from <b>theweathernetwork.com</b>.

## Files
1. <b>Dashboard:</b> this dashboard uses Stremalit to present the data found within <b>streamlit_website.py</b>

2. <b>models and accuracy metrics:</b> The model, metrics, and explainer (SHAP and LIME) can be found within pickle files:
Models were created and saved in <b>test_AI.py</b>.

<u>Model</u>: 
- weather_model.pkl

<u>Metrics</u>:
- accuracy.pkl
- f1.pkl
- precision.pkl
- recall.pkl
- train_accuracy.pkl

<u>DataFrame</u>:
- emission.pkl

<u>Explainer</u>:
- explainer.pkl
- lime_explainer.pkl
- weather_shap_values.pkl

## Data Source
- Weather data for Eltham was collected using the <b>request</b> module from weatherapi.com 
- Greenhouse Emission Data was published by the United Nation on the UNData site (data.un.org, n.d.). 


## Packages
The packages for this project can be found within <b>requirements.txt</b> listed here: 

- streamlit==1.30.0
- pandas==2.0.3
- requests==2.31.0
- scipy==1.11.2
- bokeh==2.4.3
- plotly==5.17.0
- scikit-learn==1.2.2
- imbalanced_learn==0.12.0
- category_encoders==2.3.0
- numpy==1.23.5
- shap==0.45.1
- streamlit_shap==1.0.2

## Reference list

data.un.org. (n.d.). UNdata | explorer. [online] Available at: http://data.un.org/Explorer.aspx.

Harboure, P. (2024). WEATHER CLIMATE WATER WMO Global Annual to Decadal Climate Update 2024-2028. [online] Available at: https://library.wmo.int/viewer/68910/download?file=WMO_GADCU_2024-2028_en.pdf&type=pdf&navigator=1.
