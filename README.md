# Temperature Trends Viz

A web-based tool for visualizing and analyzing temperature trends for cities around the world using historical weather data.

## Features

- **Single City Analysis**: Detailed view with monthly and annual temperature trends
- **Multi-City Comparison**: Compare temperature trends across multiple cities
- **Customizable Time Range**: Analyze data from 1990 to present
- **Interactive Visualizations**: Built with Streamlit for easy interaction
- **Configurable City Database**: Easily add or modify cities via JSON configuration

## Prerequisites

Make sure you have [uv](https://docs.astral.sh/uv/) installed. If not, install it:

```bash
# On macOS and Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# On Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Or with pip
pip install uv
```

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd temperature-trends-viz
```

2. Install dependencies using uv:
```bash
# Install all dependencies
uv sync

# Or install in development mode with dev dependencies
uv sync --extra dev
```

## Usage

### Method 1: Using uv run (Recommended)

```bash
# Run the application directly with uv
uv run streamlit run weather_gui.py
```

### Method 2: Using virtual environment

```bash
# Activate the virtual environment created by uv
source .venv/bin/activate  # On Linux/macOS
# or
.venv\Scripts\activate     # On Windows

# Run the application
streamlit run weather_gui.py
```

### Method 3: Using the convenience script

```bash
# Make the script executable (Linux/macOS only)
chmod +x run.sh

# Run the application
./run.sh
```

After starting the application:

1. Open your browser and navigate to the displayed URL (usually `http://localhost:8501`)

2. Use the sidebar to:
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

## Development

### Setting up development environment

```bash
# Install with development dependencies
uv sync --extra dev

# Run code formatting
uv run black weather_gui.py
uv run isort weather_gui.py

# Run type checking
uv run mypy weather_gui.py

# Run linting
uv run flake8 weather_gui.py
```

### Adding new dependencies

```bash
# Add a new runtime dependency
uv add package-name

# Add a new development dependency
uv add --group dev package-name

# Remove a dependency
uv remove package-name
```

## Requirements

- Python 3.8+
- uv package manager
- Dependencies managed via pyproject.toml:
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
## Quick Start

For the impatient, here's the fastest way to get started:

```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone and run
git clone <repository-url>
cd temperature-trends-viz
uv run streamlit run weather_gui.py
```

That's it! The application will automatically install dependencies and start running.

## Verify Setup

To check if everything is configured correctly, run the setup verification script:

```bash
# Test your setup
python test_setup.py

# Or with uv
uv run python test_setup.py
```

This will check:
- Python version compatibility
- Required dependencies
- Project files
- uv installation
- Virtual environment setup

For detailed setup instructions, see [SETUP.md](SETUP.md).
