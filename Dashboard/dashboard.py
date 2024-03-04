!pip install matplotlib
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

def create_daily_rent_df(df):
    daily_rent_df = df.resample(rule='D', on='dteday').agg({
        "casual": "sum",
        "registered": "sum"
    })
    daily_rent_df = daily_rent_df.reset_index()
    daily_rent_df.rename(columns={
        "cnt": "casual",
        "cnt": "registered"
    }, inplace=True)
    
    return daily_rent_df

day_df = pd.read_csv("day_data.csv")
hour_df = pd.read_csv("hour_data.csv")

datetime_columns = ["dteday"]
day_df.sort_values(by="dteday", inplace=True)
day_df.reset_index(inplace=True)
 
for column in datetime_columns:
  day_df[column] = pd.to_datetime(day_df[column])
  min_date = day_df["dteday"].min()
max_date = day_df["dteday"].max()
 
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://github.com/stefanyy15/Analisis-Data/blob/c034093ef1a60da26d64209adc1013f381fab590/bikee.jpg")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = day_df[(day_df["dteday"] >= str(start_date)) & 
(day_df["dteday"] <= str(end_date))]


daily_rent_df = create_daily_rent_df(main_df)

st.header('Bike Sharing Dicoding 68 :sparkles:')
st.subheader('Daily Rent')

col1, col2 = st.columns(2)
with col1:
    daily_rent = daily_rent_df.casual.sum()
    st.metric("Daily Rent Casual", value=daily_rent)

with col2:
    daily_rent = daily_rent_df.registered.sum()
    st.metric("Daily Rent Registered", value=daily_rent)  

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    daily_rent_df["dteday"],
    daily_rent_df["registered"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)


st.write("Grafik Variabel:")
sns.set(style="whitegrid")
fig, axes = plt.subplots(2, 2, figsize=(12, 8))
sns.histplot(day_df['temp'], ax=axes[0, 0], kde=True)
axes[0, 0].set_title('Temperature Distribution')
sns.lineplot(x='season', y='cnt', data=day_df, ax=axes[0, 1])
axes[0, 1].set_title('Bike Rentals by Season')
sns.lineplot(x='hr', y='cnt', hue='workingday', data=hour_df, ax=axes[1, 0])
axes[1, 0].set_title('Hourly Bike Rentals')
sns.lineplot(x='mnth', y='cnt', hue='yr', data=day_df, ax=axes[1, 1])
axes[1, 1].set_title('Monthly Bike Rentals')
plt.tight_layout()
st.pyplot(fig)

def map_season_to_name(season_number):
    season_names = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
    return season_names.get(season_number, 'Unknown')


# Tampilkan filter interaktif
st.sidebar.header('Filter Data')
selected_season_number = st.sidebar.selectbox('Select Season', day_df['season'].unique())
selected_season_name = map_season_to_name(selected_season_number)
selected_day = st.sidebar.selectbox('Select Day', day_df['weekday'].unique())
selected_weather = st.sidebar.selectbox('Select Weather', day_df['weathersit'].unique())

# Terapkan filter
filtered_data = day_df[(day_df['season'] == selected_season_number) & (day_df['weekday'] == selected_day) & (day_df['weathersit'] == selected_weather)]

# Tampilkan tabel data terfilter
st.write("Data Terfilter:")
st.write(filtered_data)
