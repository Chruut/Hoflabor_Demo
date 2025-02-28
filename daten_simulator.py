import pandas as pd
import numpy as np

#  Definition of Simulation parameters
fields = ["Karotten", "Pastinaken", "Nutzhanf", "Kartoffeln", "Karotten"]
n_sensors = len(fields) # Each field has sensors for data collection
hours_per_day = 24
days_per_year = 365
total_hours = hours_per_day * days_per_year  # Total hours in a year
start_time = pd.Timestamp("2024-01-01 00:00")

####################### Simulating Data Points #####################
# Baseline long-term movement
base_temp = 10 * np.sin(0.15 * np.linspace(-2, 25, days_per_year)) + 15  # Seasonal Temperature Movement
base_humidity = np.linspace(80, 50, days_per_year)  # Seasonal Soil Humidity Movement

# Adding Variability into the data
records = []
for hour in range(total_hours):
    timestamp = start_time + pd.Timedelta(hours=hour)
    day_of_year = hour // hours_per_day  # Correct calculation for day_of_year
    for n, field in enumerate(fields, start=1):
        # Variation per Feld and Hour
        temp_variation = np.random.normal(0, 2)  # Random Temperature Fluctuations
        humidity_variation = np.random.normal(0, 5)  # Random Humidity Fluctuations
        plant_effect = np.sin((day_of_year / days_per_year) * 5 * np.pi) * np.random.uniform(-3, 3) # Additional Fluctuations for each field independently

        # Bringing Sub-Fluctuations together
        temperature = base_temp[day_of_year] + temp_variation + plant_effect
        humidity = base_humidity[day_of_year] + humidity_variation - plant_effect

         # Generate Divesity-Index Values (0-100)
        if field == "Nutzhanf":
            diversitaet = np.clip(np.random.normal(70, 15), 50, 100).astype(int)  # Mean is 70, limited to a Range of 50-100
        else:
            diversitaet = np.clip(np.random.normal(40, 20), 10, 80).astype(int)  # Mean is 40, limited to a Range of 10-80
        
        records.append([timestamp, temperature, humidity,diversitaet, field, n,day_of_year+1])
        

############################## Create the DataFrame ##########################
df = pd.DataFrame(records, columns=["Zeit", "Temperatur", "Feuchtigkeit", "Diversitaets-Index", "Feldtyp", "Feld", "Jahrestag"])
df[["Temperatur", "Feuchtigkeit"]] = df[["Temperatur", "Feuchtigkeit"]].round(2) # Reducing float
df = df.fillna(0) # Replaces any NAs with 0


# Dealing with Time Crap
df['Zeit'] = pd.to_datetime(df['Zeit'])  # Security check for the correct time format ('datetime')
df['Tag'] = df['Zeit'].dt.day  # Day of the Month (1–31)
df['Woche'] = df['Zeit'].dt.isocalendar().week  # Yearly Calendary Weeks (1–53)
df['Monat'] = df['Zeit'].dt.month  # Month as Number (1–12)
df['Feld'] = pd.to_numeric(df['Feld'], errors='coerce')  # Conversion


# Save as CSV file
df.to_csv("Hoflabor_Demo/zoo_data.csv", index=False)

# Bring the information to the public
print(df.head())
