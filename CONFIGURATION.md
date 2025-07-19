# Configuration Guide

## Adding New Cities

The `cities.json` file contains all the cities available in the Temperature Trends Viz. You can easily add new cities by editing this file.

### JSON Structure

Each city entry follows this format:

```json
{
  "City Name": {
    "lat": latitude_in_decimal_degrees,
    "lon": longitude_in_decimal_degrees
  }
}
```

### Example: Adding New York

```json
{
  "New York": {
    "lat": 40.7128,
    "lon": -74.0060
  }
}
```

### Finding Coordinates

You can find city coordinates using:

1. **Google Maps**: Right-click on a location and copy the coordinates
2. **Wikipedia**: Most city pages include coordinates
3. **GeoNames**: http://www.geonames.org/
4. **LatLong.net**: https://www.latlong.net/

### Important Notes

- **Latitude**: Ranges from -90 to +90 (negative for South, positive for North)
- **Longitude**: Ranges from -180 to +180 (negative for West, positive for East)
- **Precision**: Use at least 4 decimal places for accuracy
- **City Names**: Use clear, recognizable names (avoid special characters if possible)

### Example Multi-Country Configuration

```json
{
  "Beijing": {
    "lat": 39.9042,
    "lon": 116.4074
  },
  "Tokyo": {
    "lat": 35.6762,
    "lon": 139.6503
  },
  "London": {
    "lat": 51.5074,
    "lon": -0.1278
  },
  "New York": {
    "lat": 40.7128,
    "lon": -74.0060
  },
  "Sydney": {
    "lat": -33.8688,
    "lon": 151.2093
  }
}
```

### After Adding Cities

1. Save the `cities.json` file
2. Restart the Streamlit application
3. The new cities will appear in the dropdown menus

### Data Availability

Note that not all locations have complete weather data. The Meteostat database coverage varies by:

- **Geographic location**: Major cities typically have better coverage
- **Time period**: Recent years have more complete data
- **Weather stations**: Remote areas may have limited data

The application will handle missing data gracefully and show warnings when data is unavailable.
