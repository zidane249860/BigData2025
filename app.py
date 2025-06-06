import streamlit as st
import pandas as pd
from prophet import Prophet
import plotly.express as px

st.set_page_config(page_title="Stock Price Forecast", layout="centered")
st.title("📈 Stock Price Forecast (Next 10 Days)")

# Load your CSV data
df = pd.read_csv("stocks.csv")

# Convert Scraped At to datetime
df["Scraped At"] = pd.to_datetime(df["Scraped At"], errors="coerce")

# Ensure Price is float (skip string cleanup if already clean)
if df["Price"].dtype == object:
    df["Price"] = (
        df["Price"]
        .str.replace("Rp", "", regex=False)
        .str.replace(",", "", regex=False)
        .str.replace(" ", "")  # for non-breaking space
        .str.strip()
        .astype(float)
    )


# Dropdown for company selection
companies = sorted(df["Company"].unique())
selected_company = st.selectbox("Select a company to forecast", companies)

# Filter for selected company
company_df = df[df["Company"] == selected_company][["Scraped At", "Price"]].rename(
    columns={"Scraped At": "ds", "Price": "y"}
)

#(Debug) Checking the latest data timestamp
st.write("Latest date in data:", company_df['ds'].max())

# Check for enough data
if len(company_df) < 10:
    st.warning("Not enough data to forecast.")
else:
    # Train Prophet model
    model = Prophet()
    company_df = company_df.dropna(subset=['ds', 'y']).sort_values("ds")
    model.fit(company_df)

    # Predict next 10 days
    future = model.make_future_dataframe(periods=10, freq='D')
    forecast = model.predict(future)

    # Plot forecast using Plotly
    fig = px.line(forecast, x="ds", y="yhat", labels={"ds": "Date", "yhat": "Predicted Price (Rp)"},
                  title=f"{selected_company} - 10-Day Forecast")
    st.plotly_chart(fig, use_container_width=True)
