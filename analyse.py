import pandas as pd

# Load the preprocessed data
df = pd.read_csv('df_preprocessedknn.csv')

# Print the number of rows and columns
print(f'Number of rows: {df.shape[0]}')
print(f'Number of columns: {df.shape[1]}')

# Print the first 5 rows to check the data
print(df.head())

# Print the summary statistics
print(df.describe())

# Print the number of unique values in each column
# for col in df.columns:
#     print(f'Number of unique values in {col}: {df[col].nunique()}')