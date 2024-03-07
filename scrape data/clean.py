import pandas as pd

# Read the CSV file
df = pd.read_csv('mitNEW.csv')

# Remove extra spaces from the 'Course Title' column
df['Course Title'] = df['Course Title'].str.replace('\s+', ' ', regex=True).str.strip()

# Write the cleaned data back to the CSV file
df.to_csv('mitNEW1.csv', index=False)