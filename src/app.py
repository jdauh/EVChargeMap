import streamlit as st
import pandas as pd

DATA_URL = 'https://www.data.gouv.fr/fr/datasets/r/8d9398ae-3037-48b2-be19-412c24561fbb'
KW_COLUMN = 'puissance_nominale'
OP_COLUMN = 'nom_operateur'
MIN_POWER = 0
MAX_POWER = 60000
STEP_POWER = 500

@st.cache_data
def load_data(url: str) -> pd.DataFrame:
    """Load and clean the data from the provided URL."""
    try:
        df = pd.read_csv(url)
        df.rename(columns={'consolidated_longitude': 'longitude', 'consolidated_latitude': 'latitude'}, inplace=True)
        return df
    
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

st.title('EV charging stations in France')
st.text('Loading data...')

df = load_data(DATA_URL)
st.text('Data loading completed!')

# A checkbow to show/hide the raw data
if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.dataframe(df)

# Preparing the data for the chart : cast float to int, count stations per power capacity, rename columns, new index
power_data = df[KW_COLUMN].astype(int)
chart_data = power_data.value_counts().reset_index()
chart_data.columns = ['Power', 'Count']
chart_data.set_index('Power', inplace=True)

st.subheader('Number of stations per nominal power declared (kW)')
st.bar_chart(chart_data)

# Filter data and display a map
# If no operator is selected, we show all operators data in the map
station_types = st.multiselect('Filter the map by operator:', options=df[OP_COLUMN].unique())
min_power, max_power = st.slider('Filter the map by power range (kW):', min_value=MIN_POWER, max_value=MAX_POWER, value=(MIN_POWER, MAX_POWER), step=STEP_POWER)
map_data = df[df[OP_COLUMN].isin(station_types) & df[KW_COLUMN].between(min_power, max_power) if station_types else df[KW_COLUMN].between(min_power, max_power)]
st.map(map_data[['latitude', 'longitude']])

# Preparing the data for the table : cast float to int, count stations per operator, rename columns, new index
operator_data = df[OP_COLUMN].value_counts().reset_index()
operator_data.columns = ['Operator', 'Count']
operator_data.set_index('Operator', inplace=True)

st.subheader('Number of stations per operator')
st.dataframe(operator_data)

# Display the data source with a link
st.markdown('<a href="https://www.data.gouv.fr/fr/datasets/fichier-consolide-des-bornes-de-recharge-pour-vehicules-electriques/" target="_blank">Source : DataGouv.fr</a>', unsafe_allow_html=True)
