import streamlit as st
from meteostat import Monthly, Point
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.font_manager as fm

# Configure page
st.set_page_config(
    page_title="Weather Data Visualization",
    page_icon="🌡️",
    layout="wide"
)

# Hide Streamlit's hamburger menu, deploy button and footer
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
.stDeployButton {visibility: hidden;}
[data-testid="stAppDeployButton"] {visibility: hidden;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# City coordinates dictionary
CITIES = {
    "Beijing": Point(39.9042, 116.4074),
    "Taiyuan": Point(37.8706, 112.5489),
    "Chengdu": Point(30.5728, 104.0668),
    "Chongqing": Point(29.5630, 106.5516),
    "Hangzhou": Point(30.2741, 120.1551),
    "Guangzhou": Point(23.1291, 113.2644),
    "Shenzhen": Point(22.5431, 114.0579),
    "Xi'an": Point(34.3416, 108.9398),
    "Tianjin": Point(39.1422, 117.1767),
    "Haikou": Point(20.0458, 110.3417),
    "Sanya": Point(18.2529, 109.5119),
    "Shanghai": Point(31.2304, 121.4737),
    "Qingdao": Point(36.0671, 120.3826),
    "Suzhou": Point(31.2989, 120.5853),
    "Xiamen": Point(24.4798, 118.0894),
    "Kunming": Point(25.0389, 102.7183),
    "Shenyang": Point(41.8057, 123.4315),
    "Changchun": Point(43.8913, 125.3313),
    "Harbin": Point(45.7000, 126.6000),
    "Lanzhou": Point(36.0611, 103.8343),
    "Urumqi": Point(43.8000, 87.6000),
    "Nanning": Point(22.8167, 108.3167),
    "Lhasa": Point(29.6500, 91.1000),
    "Hong Kong": Point(22.3000, 114.2000),
    "Macau": Point(22.2000, 113.5000),
    "Zhengzhou": Point(34.7466, 113.6253),
    "Jinan": Point(36.6512, 117.1201),
    "Shijiazhuang": Point(38.0428, 114.5149),
    "Yinchuan": Point(38.4872, 106.2309),
    "Xining": Point(36.6171, 101.7782),
    "Guiyang": Point(26.5783, 106.7135),
    "Changsha": Point(28.2282, 112.9388)
}

def get_weather_data(city_point, start_year, end_year):
    """Get weather data for a specific city and time range"""
    start = datetime(start_year, 1, 1)
    end = datetime(end_year, 12, 31)
    
    try:
        data = Monthly(city_point, start, end).fetch()
        if data.empty:
            return None
        
        df = data[['tavg']].reset_index()
        df['Year'] = df['time'].dt.year
        df['Month'] = df['time'].dt.month
        df = df.drop(columns='time').dropna()
        
        # Calculate annual average temperature
        annual_avg = df.groupby('Year')['tavg'].mean().reset_index()
        
        return df, annual_avg
    except Exception as e:
        st.error(f"Error fetching data: {str(e)}")
        return None

def create_temperature_plot(city_name, df, annual_avg, start_year, end_year):
    """Create temperature plot for a specific city"""
    fig, ax = plt.subplots(figsize=(14, 8))
    
    # Set style
    sns.set_style("whitegrid")
    
    # Plot monthly trends
    for m in range(1, 13):
        month_data = df[df['Month'] == m]
        if not month_data.empty:
            ax.plot(month_data['Year'], month_data['tavg'],
                   label=f'Month {m}', alpha=0.7, linewidth=1)
    
    # Plot annual average trend (bold line)
    if not annual_avg.empty:
        ax.plot(annual_avg['Year'], annual_avg['tavg'],
               label='Annual Average', color='red', linewidth=3, alpha=0.9)
    
    ax.set_title(f'{city_name} Monthly Average Temperature Trends ({start_year}-{end_year})')
    ax.set_xlabel('Year')
    ax.set_ylabel('Average Temperature (°C)')
    ax.legend(title='Month', ncol=4, loc='upper left')
    ax.grid(True)
    
    plt.tight_layout()
    return fig

def create_comparison_plot(selected_cities, start_year, end_year):
    """Create comparison plot for multiple cities"""
    import matplotlib.cm as cm
    import numpy as np
    import time

    # No need to limit here as UI already limits to 10 cities

    fig, ax = plt.subplots(figsize=(14, 8))

    # Use different colormaps for better distinction
    if len(selected_cities) <= 10:
        colors = cm.tab10(np.linspace(0, 1, 10))
    else:
        colors = cm.tab20(np.linspace(0, 1, 20))

    successful_plots = 0

    for i, city_name in enumerate(selected_cities):
        try:
            city_point = CITIES[city_name]

            # Add small delay to prevent API rate limiting
            if i > 0:
                time.sleep(0.1)

            result = get_weather_data(city_point, start_year, end_year)

            if result:
                df, annual_avg = result
                if not annual_avg.empty and len(annual_avg) > 0:
                    # Validate data quality
                    if annual_avg['tavg'].min() > -50 and annual_avg['tavg'].max() < 50:
                        ax.plot(annual_avg['Year'], annual_avg['tavg'],
                               label=city_name, color=colors[i % len(colors)],
                               linewidth=2, alpha=0.8)
                        successful_plots += 1
                    else:
                        st.warning(f"⚠️ Suspicious data detected for {city_name}, skipping...")
        except Exception as e:
            st.warning(f"⚠️ Error processing {city_name}: {str(e)}")
            continue

    if successful_plots == 0:
        st.error("No valid data could be plotted for the selected cities and time range.")
        return None

    ax.set_title(f'Cities Annual Average Temperature Comparison ({start_year}-{end_year})')
    ax.set_xlabel('Year')
    ax.set_ylabel('Average Temperature (°C)')

    # Optimize legend for many cities
    if len(selected_cities) <= 6:
        ax.legend(title='City', loc='best')
    else:
        ax.legend(title='City', bbox_to_anchor=(1.05, 1), loc='upper left')

    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    return fig

# Streamlit UI
st.title("🌡️ Weather Data Visualization")
st.markdown("Explore temperature trends for major Chinese cities")

# Sidebar for controls
st.sidebar.header("Settings")

# City selection
st.sidebar.subheader("City Selection")
view_mode = st.sidebar.radio(
    "View Mode:",
    ["Single City", "Compare Cities"]
)

# Sort cities alphabetically for better user experience
sorted_cities = sorted(list(CITIES.keys()))

if view_mode == "Single City":
    selected_city = st.sidebar.selectbox(
        "Select a city:",
        sorted_cities
    )
else:
    selected_cities = st.sidebar.multiselect(
        "Select cities to compare (max 10):",
        sorted_cities,
        default=["Beijing", "Shanghai", "Guangzhou", "Shenzhen"],
        max_selections=10
    )

# Year selection
st.sidebar.subheader("Time Range")
current_year = datetime.now().year
start_year = st.sidebar.number_input(
    "Start Year:",
    min_value=1990,
    max_value=current_year-1,
    value=1990,
    step=1
)

end_year = st.sidebar.number_input(
    "End Year:",
    min_value=start_year+1,
    max_value=current_year,
    value=current_year-1,
    step=1
)

# Validate year range
if end_year <= start_year:
    st.sidebar.error("End year must be greater than start year!")
    st.stop()

# Generate plot button
if st.sidebar.button("Generate Plot", type="primary"):
    with st.spinner("Fetching weather data and generating plot..."):
        
        if view_mode == "Single City":
            # Single city view
            city_point = CITIES[selected_city]
            result = get_weather_data(city_point, start_year, end_year)
            
            if result:
                df, annual_avg = result
                fig = create_temperature_plot(selected_city, df, annual_avg, start_year, end_year)
                st.pyplot(fig)
                
                # Display some statistics
                st.subheader("Statistics")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    avg_temp = annual_avg['tavg'].mean()
                    st.metric("Average Temperature", f"{avg_temp:.1f}°C")
                
                with col2:
                    max_temp = annual_avg['tavg'].max()
                    max_year = annual_avg[annual_avg['tavg'] == max_temp]['Year'].iloc[0]
                    st.metric("Highest Annual Avg", f"{max_temp:.1f}°C", f"in {max_year}")
                
                with col3:
                    min_temp = annual_avg['tavg'].min()
                    min_year = annual_avg[annual_avg['tavg'] == min_temp]['Year'].iloc[0]
                    st.metric("Lowest Annual Avg", f"{min_temp:.1f}°C", f"in {min_year}")
            else:
                st.error("Failed to fetch data for the selected city and time range.")
        
        else:
            # Multiple cities comparison
            if not selected_cities:
                st.warning("Please select at least one city for comparison.")
            else:
                fig = create_comparison_plot(selected_cities, start_year, end_year)
                if fig:
                    st.pyplot(fig)

                    # Display comparison statistics

                    st.subheader("Comparison Statistics")
                    stats_data = []

                    for city_name in selected_cities:
                        try:
                            city_point = CITIES[city_name]
                            result = get_weather_data(city_point, start_year, end_year)

                            if result:
                                df, annual_avg = result
                                if not annual_avg.empty:
                                    # Validate data quality before calculating stats
                                    if annual_avg['tavg'].min() > -50 and annual_avg['tavg'].max() < 50:
                                        avg_temp = annual_avg['tavg'].mean()
                                        max_temp = annual_avg['tavg'].max()
                                        min_temp = annual_avg['tavg'].min()

                                        stats_data.append({
                                            'City': city_name,
                                            'Average Temperature (°C)': f"{avg_temp:.1f}",
                                            'Highest Annual Avg (°C)': f"{max_temp:.1f}",
                                            'Lowest Annual Avg (°C)': f"{min_temp:.1f}"
                                        })
                        except Exception as e:
                            st.warning(f"Error calculating stats for {city_name}: {str(e)}")
                            continue

                    if stats_data:
                        stats_df = pd.DataFrame(stats_data)
                        # Reset index to start from 1 instead of 0
                        stats_df.index = range(1, len(stats_df) + 1)
                        st.dataframe(stats_df, use_container_width=True)
                    else:
                        st.error("No valid statistics could be calculated for the selected cities.")

# Information section
st.sidebar.markdown("---")
st.sidebar.markdown("### About")
st.sidebar.markdown("""
This app visualizes temperature trends for major Chinese cities using data from Meteostat.

**Features:**
- Single city detailed view with monthly and annual trends
- Multi-city comparison view
- Customizable time range
- Real-time data generation
""")
