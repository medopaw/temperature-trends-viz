# Temperature Trends Viz

A web-based tool for visualizing and analyzing temperature trends for cities around the world using historical weather data.

## Features

- **Single City Analysis**: Detailed view with monthly and annual temperature trends
- **Multi-City Comparison**: Compare temperature trends across multiple cities
- **Customizable Time Range**: Analyze data from 1990 to present
- **Interactive Visualizations**: Built with Streamlit for easy interaction
- **Configurable City Database**: Easily add or modify cities via JSON configuration

## Quick Start

### Option 1: Docker (Fastest - No Installation Required)

```bash
# Run directly from Docker Hub
docker run -p 8501:8501 --name temperature-trends-viz medopaw/temperature-trends-viz:latest
```

Then open your browser to `http://localhost:8501`

### Option 2: Local Development

```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone and run
git clone https://github.com/medopaw/temperature-trends-viz.git
cd temperature-trends-viz
uv run streamlit run weather_gui.py
```

That's it! The application will automatically install dependencies and start running.

## Adding New Cities

To add new cities, edit `cities.json`:

```json
{
  "Your City": {
    "lat": 40.7128,
    "lon": -74.0060
  }
}
```

Save the file and restart the application.

## Usage

After starting the application:

1. Open your browser and navigate to the displayed URL (usually `http://localhost:8501`)
2. Use the sidebar to:
   - Select single city or comparison mode
   - Choose cities to analyze
   - Set the time range
   - Generate visualizations

## Data Source

This application uses the [Meteostat](https://meteostat.net/) library to fetch historical weather data from meteorological stations worldwide.

## Documentation

- **[SETUP.md](SETUP.md)** - Detailed local development setup guide
- **[DOCKER.md](DOCKER.md)** - Complete Docker usage and deployment guide

## Requirements

- Python 3.8+
- Dependencies: streamlit, meteostat, pandas, matplotlib, seaborn

## License

This project is open source and available under the MIT License.

## Contributing

Feel free to contribute by:
- Adding more cities to the database
- Improving visualizations
- Adding new features
- Reporting bugs or issues
