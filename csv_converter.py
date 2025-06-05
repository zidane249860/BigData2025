import pandas as pd

# Load CSV
with open("stocks.csv", encoding="utf-8", errors="replace") as f:
    df = pd.read_csv(f)

print(df.head())

# Clean price: remove currency symbols and format as float
df["Price"] = df["Price"].str.replace("Rp", "").str.replace(",", "").str.replace(" ", "").astype(float)

# Convert timestamp to datetime
df["Scraped At"] = pd.to_datetime(df["Scraped At"], format="mixed", dayfirst=False, errors="coerce")

# Save cleaned data back to CSV
df.to_csv("stocks.csv", index=False, encoding="utf-8")