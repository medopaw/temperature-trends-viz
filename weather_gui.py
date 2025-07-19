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

# City coordinates dictionary
CITIES = {
    "Beijing": Point(39.9042, 116.4074),
    "Taiyuan": Point(37.8706, 112.5489),
    "Chengdu": Point(30.5728, 104.0668),
    "Chongqing": Point(29.5630, 106.5516),
    "Hangzhou": Point(30.2741, 120.1551),
    "Guangzhou": Point(23.1291, 113.2644)
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
    fig, ax = plt.subplots(figsize=(14, 8))
    
    colors = ['red', 'blue', 'green', 'orange', 'purple', 'brown']
    
    for i, city_name in enumerate(selected_cities):
        city_point = CITIES[city_name]
        result = get_weather_data(city_point, start_year, end_year)
        
        if result:
            df, annual_avg = result
            if not annual_avg.empty:
                ax.plot(annual_avg['Year'], annual_avg['tavg'],
                       label=city_name, color=colors[i % len(colors)], 
                       linewidth=2, alpha=0.8)
    
    ax.set_title(f'Cities Annual Average Temperature Comparison ({start_year}-{end_year})')
    ax.set_xlabel('Year')
    ax.set_ylabel('Average Temperature (°C)')
    ax.legend(title='City')
    ax.grid(True)
    
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

if view_mode == "Single City":
    selected_city = st.sidebar.selectbox(
        "Select a city:",
        list(CITIES.keys())
    )
else:
    selected_cities = st.sidebar.multiselect(
        "Select cities to compare:",
        list(CITIES.keys()),
        default=["Beijing", "Guangzhou"]
    )

# Year selection
st.sidebar.subheader("Time Range")
current_year = datetime.now().year
start_year = st.sidebar.number_input(
    "Start Year:",
    min_value=1990,
    max_value=current_year-1,
    value=1995,
    step=1
)

end_year = st.sidebar.number_input(
    "End Year:",
    min_value=start_year+1,
    max_value=current_year,
    value=2024,
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
                st.pyplot(fig)
                
                # Display comparison statistics
                st.subheader("Comparison Statistics")
                stats_data = []
                
                for city_name in selected_cities:
                    city_point = CITIES[city_name]
                    result = get_weather_data(city_point, start_year, end_year)
                    
                    if result:
                        df, annual_avg = result
                        if not annual_avg.empty:
                            avg_temp = annual_avg['tavg'].mean()
                            max_temp = annual_avg['tavg'].max()
                            min_temp = annual_avg['tavg'].min()
                            
                            stats_data.append({
                                'City': city_name,
                                'Average Temperature (°C)': f"{avg_temp:.1f}",
                                'Highest Annual Avg (°C)': f"{max_temp:.1f}",
                                'Lowest Annual Avg (°C)': f"{min_temp:.1f}"
                            })
                
                if stats_data:
                    stats_df = pd.DataFrame(stats_data)
                    st.dataframe(stats_df, use_container_width=True)

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
