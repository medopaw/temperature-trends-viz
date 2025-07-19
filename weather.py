from meteostat import Monthly, Point
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Define Guangzhou coordinates
guangzhou = Point(23.1291, 113.2644)

# Time range
start = datetime(1995, 1, 1)
end = datetime(2024, 12, 31)

# Get data
data = Monthly(guangzhou, start, end).fetch()
df = data[['tavg']].reset_index()
df['Year'] = df['time'].dt.year
df['Month'] = df['time'].dt.month
df = df.drop(columns='time').dropna()

# Calculate annual average temperature
annual_avg = df.groupby('Year')['tavg'].mean().reset_index()

# Create plot
plt.figure(figsize=(14, 8))
sns.set(style="whitegrid")

# Plot monthly trends
for m in range(1, 13):
    plt.plot(df[df['Month'] == m]['Year'], df[df['Month'] == m]['tavg'],
             label=f'Month {m}', alpha=0.7, linewidth=1)

# Plot annual average trend (bold line)
plt.plot(annual_avg['Year'], annual_avg['tavg'],
         label='Annual Average', color='red', linewidth=3, alpha=0.9)

plt.title('Guangzhou Monthly Average Temperature Trends (1995-2024)')
plt.xlabel('Year')
plt.ylabel('Average Temperature (°C)')
plt.legend(title='Month', ncol=4, loc='upper left')
plt.tight_layout()
plt.grid(True)
plt.show()
