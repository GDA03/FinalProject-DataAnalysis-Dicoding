# dashboard.py

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Set the Streamlit layout to wide
st.set_page_config(layout="wide")

# Load datasets
dfh = pd.read_csv('data/hour.csv')
dfd = pd.read_csv('data/day.csv')

# Mapping season and holiday for readability (for hourly dataset)
season_map = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
dfh['season'] = dfh['season'].map(season_map)
holiday_map = {0: 'Non-Holiday', 1: 'Holiday'}
dfh['holiday'] = dfh['holiday'].map(holiday_map)

with st.sidebar:
    st.write(
        """
            # Bike Sharing Dashboard
            Bike Sharing Data Analysis Project

            Gerald Dustin Albert - Bangkit Academy
        """
    )

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", [
    "Season & Holidays", 
    "Holidays & non-holidays", 
    "Most bycicles rental in season", 
    "Most significant factors rush hours"
])

# Rentals by Hour (Season and Holiday)
if page == "Season & Holidays":
    st.header("Bike Rentals by Hour")
    
    
    st.write(
    """
### Question 1
How do bike rentals vary across different seasons and holidays?

1. **Bike Rentals by Hour and Season**:
   - The bar chart shows clear **hourly patterns** of bike usage across different seasons.
   - Bike rentals peak around **8 AM** and **5-6 PM**, coinciding with typical commuting hours.
   - **Summer and Fall** see the highest rental activity, reflecting favorable weather and increased outdoor activity.
   
2. **Bike Rentals by Hour (Holiday vs Non-Holiday)**:
   - On **holidays**, rentals are more evenly distributed throughout the day, with smaller peaks.
   - On **non-holidays**, peaks are prominent during **commuting hours**, showing a pattern of work-related travel.

This suggests that bike rentals are heavily influenced by seasonality and commuting behaviors, with higher usage during warmer months and workdays.
    """
)
    # Season Plot
    st.subheader("Rentals by Hour of Day for Different Seasons")
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x='hr', y='cnt', hue='season', data=dfh, errorbar=None, ax=ax)
    ax.set_title('Bike Rentals by Hour and Season')
    ax.set_xlabel('Hour of Day')
    ax.set_ylabel('Total Rentals')
    st.pyplot(fig)

    # Holiday Plot
    st.subheader("Rentals by Hour of Day on Holidays vs Non-Holidays")
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x='hr', y='cnt', hue='holiday', data=dfh, errorbar=None, ax=ax)
    ax.set_title('Bike Rentals by Hour on Holidays vs Non-Holidays')
    ax.set_xlabel('Hour of Day')
    ax.set_ylabel('Total Rentals')
    st.pyplot(fig)

    # Plotly interactive chart
    st.subheader("Interactive Plot: Rentals by Hour and Season/Holiday")
    fig = make_subplots(rows=1, cols=2, subplot_titles=('Bike Rentals by Hour and Season', 'Bike Rentals by Hour and Holiday'))

    # Bar chart for rentals by hour and season
    season_counts = dfh.groupby(['hr', 'season'])['cnt'].sum().reset_index()
    fig.add_trace(
        go.Bar(x=season_counts['hr'], y=season_counts['cnt'], name='Season', marker=dict(color='blue'), text=season_counts['season']),
        row=1, col=1
    )

    # Bar chart for rentals by hour and holiday
    holiday_counts = dfh.groupby(['hr', 'holiday'])['cnt'].sum().reset_index()
    fig.add_trace(
        go.Bar(x=holiday_counts['hr'], y=holiday_counts['cnt'], name='Holiday', marker=dict(color='green'), text=holiday_counts['holiday']),
        row=1, col=2
    )

    # Update layout for Plotly figure
    fig.update_layout(
        title_text='Effect of Hourly Patterns on Bike Rentals',
        width=1000,
        height=500,
        showlegend=False
    )
    st.plotly_chart(fig)

# Rentals by Day (Holiday and Season)
elif page == "Holidays & non-holidays":
    st.header("Bike Rentals by Day")

    st.write(
    """
### Question 2
Is there a significant difference in bike usage on holidays compared to non-holidays?

1. **Average Bike Rentals (Bar Chart)**:
   - The bar chart shows that **non-holidays** have a higher average number of bike rentals compared to holidays.
   - This suggests that bike usage is more frequent on regular workdays, possibly due to commuting patterns.

2. **Distribution of Rentals (Box Plot)**:
   - The box plot reveals that **non-holidays** not only have a higher median rental count but also a wider range of usage.
   - On **holidays**, the distribution is tighter, indicating less variability in bike usage.

This indicates that bike rentals are generally lower and more consistent on holidays, while non-holidays exhibit higher and more varied usage patterns, likely driven by work-related commuting.
    """
)

    # Average rentals by holiday
    st.subheader("Average Bike Rentals on Holidays vs Non-Holidays")
    holiday_avg = dfd.groupby('holiday', observed=True)['cnt'].mean().reset_index()
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='holiday', y='cnt', data=holiday_avg, palette='Set2', ax=ax)
    ax.set_title('Average Bike Rentals: Holidays vs Non-Holidays')
    ax.set_xlabel('Day Type')
    ax.set_ylabel('Average Total Rentals')
    st.pyplot(fig)

    # Box plot: Rentals by holiday
    st.subheader("Distribution of Bike Rentals on Holidays vs Non-Holidays")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.boxplot(x='holiday', y='cnt', data=dfd, palette='Set2', ax=ax)
    ax.set_title('Distribution of Bike Rentals: Holidays vs Non-Holidays')
    ax.set_xlabel('Day Type')
    ax.set_ylabel('Total Rentals')
    st.pyplot(fig)

# Rentals by Season
elif page == "Most bycicles rental in season":
    st.header("Season with the Most Bicycle Rentals")

    st.write(
    """
### Question 3
What season are there most bicycle rentals?

- The bar chart shows the **total number of bike rentals** across the four seasons: Spring, Summer, Fall, and Winter.
- **Summer** generally sees the highest number of bike rentals, followed by **Fall** and **Spring**, indicating that warmer months have more bike activity.
- **Winter** has the lowest number of rentals, likely due to colder weather discouraging biking.

This visualization highlights how bike rentals are influenced by seasonal changes, with peak activity occurring during the warmer seasons and a significant drop during winter months.
    """
)

    # Mapping season for readability (for daily dataset)
    season_map = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
    dfd['season'] = dfd['season'].map(season_map)
    
    # Bar chart: Total rentals by season
    st.subheader("Total Bicycle Rentals by Season")
    season_totals = dfd.groupby('season')['cnt'].sum().reset_index()
    fig, ax = plt.subplots(figsize=(10, 6))
    colors = {'Spring': '#66c2a5', 'Summer': '#fc8d62', 'Fall': '#8da0cb', 'Winter': '#e78ac3'}
    bars = ax.bar(season_totals['season'], season_totals['cnt'], color=[colors[season] for season in season_totals['season']])
    ax.set_title('Total Bicycle Rentals by Season')
    ax.set_xlabel('Season')
    ax.set_ylabel('Total Rentals')
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height, f'{height:,.0f}', ha='center', va='bottom')
    st.pyplot(fig)

# Rush Hour Analysis
elif page == "Most significant factors rush hours":
    st.header("Rush Hour Analysis of Bike Rentals")
    
    st.write(
    """
### Question 4
What are the most significant factors influencing bike rentals during rush hours?

1. Temperature Effect:
   - Bike rentals tend to increase as the temperature rises during rush hours.
   - There's a clear positive correlation between warmer temperatures and more bike rentals.

2. Humidity Impact:
   - Moderate humidity levels seem to be associated with higher bike rentals.
   - Very low or very high humidity appears to discourage bike usage.

3. Windspeed Influence:
   - Lower windspeeds are generally associated with more bike rentals.
   - As windspeed increases, there's a noticeable decrease in bike rentals.

4. Working Day vs. Non-Working Day:
   - There's a significant difference in bike rentals between working and non-working days.
   - Working days see substantially higher bike rentals during rush hours, likely due to commuters.

Overall, these charts suggest that ideal conditions for high bike rentals during rush hours are:
- Warm temperatures
- Moderate humidity
- Low windspeed
- Working days

This information could be valuable for bike rental companies to predict demand and for city planners to understand commuter behavior.
    """
)
    
    # Filter rush hours data (7-9 AM and 4-7 PM)
    rush_hours = dfh[(dfh['hr'].between(7, 9)) | (dfh['hr'].between(16, 19))].copy()

    # Average rentals by temperature
    st.subheader("Average Bike Rentals by Temperature (Rush Hours)")
    rush_hours['temp_bins'] = pd.cut(rush_hours['temp'], bins=5)
    avg_temp = rush_hours.groupby('temp_bins')['cnt'].mean().reset_index()
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x='temp_bins', y='cnt', data=avg_temp, color='blue', ax=ax)
    ax.set_title('Average Bike Rentals by Temperature (Rush Hours)')
    ax.set_xlabel('Temperature (Binned)')
    ax.set_ylabel('Average Rentals')
    st.pyplot(fig)

    # Average rentals by humidity
    st.subheader("Average Bike Rentals by Humidity (Rush Hours)")
    rush_hours['hum_bins'] = pd.cut(rush_hours['hum'], bins=5)
    avg_hum = rush_hours.groupby('hum_bins')['cnt'].mean().reset_index()
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x='hum_bins', y='cnt', data=avg_hum, color='green', ax=ax)
    ax.set_title('Average Bike Rentals by Humidity (Rush Hours)')
    ax.set_xlabel('Humidity (Binned)')
    ax.set_ylabel('Average Rentals')
    st.pyplot(fig)

    # Average rentals by windspeed
    st.subheader("Average Bike Rentals by Windspeed (Rush Hours)")
    rush_hours['windspeed_bins'] = pd.cut(rush_hours['windspeed'], bins=5)
    avg_windspeed = rush_hours.groupby('windspeed_bins')['cnt'].mean().reset_index()
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x='windspeed_bins', y='cnt', data=avg_windspeed, color='orange', ax=ax)
    ax.set_title('Average Bike Rentals by Windspeed (Rush Hours)')
    ax.set_xlabel('Windspeed (Binned)')
    ax.set_ylabel('Average Rentals')
    st.pyplot(fig)

    # Average rentals by working day
    st.subheader("Average Bike Rentals by Working Day (Rush Hours)")
    avg_workingday = rush_hours.groupby('workingday')['cnt'].mean().reset_index()
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x='workingday', y='cnt', data=avg_workingday, color='purple', ax=ax)
    ax.set_title('Average Bike Rentals by Working Day (Rush Hours)')
    ax.set_xlabel('Working Day (0 = Non-Working, 1 = Working)')
    ax.set_ylabel('Average Rentals')
    st.pyplot(fig)
