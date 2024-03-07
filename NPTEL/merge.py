import pandas as pd

# Read the CSV files
df1 = pd.read_csv('NPTEL.csv', encoding='ISO-8859-1')
df2 = pd.read_csv('NPTEL1.csv', encoding='ISO-8859-1')

# Create a copy of df2's 'Course Name' column to use later
original_names = df2['Course Name'].copy()

# Convert 'Course Name' to lower case for both dataframes
df1['Course Name'] = df1['Course Name'].str.lower()
df2['Course Name'] = df2['Course Name'].str.lower()

# Concatenate the dataframes
merged_df = pd.concat([df1, df2])

# Remove duplicates based on both 'Course ID' and 'Course Name'
merged_df.drop_duplicates(subset=['Course ID', 'Course Name'], keep='first', inplace=True)

# Replace the 'Course Name' column with the original one from 'NPTEL1.csv'
merged_df.loc[merged_df['Course Name'].isin(original_names.str.lower()), 'Course Name'] = original_names

# Save to a new CSV file
merged_df.to_csv('merged.csv', index=False, encoding='utf-8')