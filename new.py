import pandas as pd
from app import description

# Load the CSV file
df = pd.read_csv('merged.csv')

df['description_gemini'] = None  # Create new column with None values

# Save the DataFrame back to the CSV file
df.to_csv('merged.csv', index=False)