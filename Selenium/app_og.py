import pandas as pd
from prophet import Prophet

# Load your cleaned CSV
df = pd.read_csv("stocks.csv")

# Convert 'Scraped At' to datetime
df["Scraped At"] = pd.to_datetime(df["Scraped At"], format="mixed")

# Filter data for one company (example: Bank Mandiri)
mandiri = df[df["Company"].str.contains("Mandiri", case=False)].copy()

# Clean and convert price
mandiri["Price"] = mandiri["Price"].str.replace("Rp", "").str.replace(",", "").astype(float)

# Prepare for Prophet
prophet_df = mandiri[["Scraped At", "Price"]].rename(columns={"Scraped At": "ds", "Price": "y"})

# Create and fit the model
model = Prophet()
model.fit(prophet_df)

# Make future dataframe (5 days ahead, assuming daily frequency)
future = model.make_future_dataframe(periods=5)

# Forecast
forecast = model.predict(future)

# Show the forecast
forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]].tail()

import matplotlib.pyplot as plt

model.plot(forecast)
plt.title("Forecast for Bank Mandiri")
plt.xlabel("Date")
plt.ylabel("Price")
plt.show()
