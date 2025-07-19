# Temperature Trends Viz

A web-based tool for visualizing and analyzing temperature trends for cities around the world using historical weather data.

## Features

- **Single City Analysis**: Detailed view with monthly and annual temperature trends
- **Multi-City Comparison**: Compare temperature trends across multiple cities
- **Customizable Time Range**: Analyze data from 1990 to present
- **Interactive Visualizations**: Built with Streamlit for easy interaction
- **Configurable City Database**: Easily add or modify cities via JSON configuration

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd temperature-trends-viz
```

2. Install required dependencies:
```bash
pip install streamlit meteostat pandas matplotlib seaborn
```

## Usage

1. Start the application:
```bash
streamlit run weather_gui.py
```

2. Open your browser and navigate to the displayed URL (usually `http://localhost:8501`)

3. Use the sidebar to:
   - Select single city or comparison mode
   - Choose cities to analyze
   - Set the time range
   - Generate visualizations

## Adding New Cities

To add new cities to the database:

1. Open `cities.json`
2. Add a new entry with the city name and coordinates:

```json
{
  "Your City": {
    "lat": 40.7128,
    "lon": -74.0060
  }
}
```

3. Save the file and restart the application

## Data Source

This application uses the [Meteostat](https://meteostat.net/) library to fetch historical weather data. Meteostat provides access to weather data from meteorological stations worldwide.

## File Structure

- `weather_gui.py` - Main application file
- `cities.json` - City coordinates database
- `README.md` - This documentation

## Requirements

- Python 3.7+
- streamlit
- meteostat
- pandas
- matplotlib
- seaborn

## License

This project is open source and available under the MIT License.

## Contributing

Feel free to contribute by:
- Adding more cities to the database
- Improving visualizations
- Adding new features
- Reporting bugs or issues

## Notes

- Data availability varies by location and time period
- Some remote locations may have limited historical data
- The application includes data validation to handle missing or suspicious data points
exakmple
