import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
file_path = 'RGU_GA data.csv'  # Ganti dengan path file yang sesuai
df = pd.read_csv(file_path)

# Convert the 'tanggal' column to datetime format
df['tanggal'] = pd.to_datetime(df['tanggal'], format='%Y%m%d')

# Define the list of sales areas
selected_areas = [
    "TEGAL", "SUKABUMI", "PURWAKARTA", "SEMARANG INNER", "SEMARANG OUTER", "MAGELANG",
    "PEKALONGAN", "KUDUS", "CIREBON", "SOLO INNER", "PURWOKERTO", "YOGYAKARTA 1",
    "BANDUNG INNER", "TASIKMALAYA", "YOGYAKARTA 2", "SOLO OUTER", "CIANJUR", "KAB. BANDUNG"
]

# Filter the dataset based on the specified sales_area labels
df_filtered = df[df['sales_area'].isin(selected_areas)]

# Streamlit app
st.title('Pelanggan Baru by Sales Area')

# Sidebar for filters
st.sidebar.title('Filters')

# Date selection in sidebar
start_date = st.sidebar.date_input('Start Date', df['tanggal'].min())
end_date = st.sidebar.date_input('End Date', df['tanggal'].max())

# Sales area selection in sidebar
sales_area_options = st.sidebar.multiselect('Select Sales Area', selected_areas, default=selected_areas)

# Filter data based on selected sales area and date range
df_selected = df_filtered[(df_filtered['sales_area'].isin(sales_area_options)) &
                          (df_filtered['tanggal'] >= pd.to_datetime(start_date)) &
                          (df_filtered['tanggal'] <= pd.to_datetime(end_date))]

# Group by day and sales_area, then sum rgu_ga_90
df_grouped = df_selected.groupby(['tanggal', 'sales_area'])['rgu_ga_90'].sum().unstack()

# Plotting the line chart
plt.figure(figsize=(14, 10))

for area in sales_area_options:
    if area in df_grouped.columns:
        plt.plot(df_grouped.index, df_grouped[area], marker='o', label=area)

plt.xlabel('Date')
plt.ylabel('Total New Customers (rgu_ga_90)')
plt.title('Daily New Customers (rgu_ga_90) by Sales Area')
plt.legend(title='Sales Area', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True)
plt.tight_layout()

# Display the plot in Streamlit
st.pyplot(plt)