import pandas as pd
from joblib import load
from sklearn.preprocessing import MinMaxScaler

# Load the model and vectorizer
model = load('modelUdemy.joblib')
vectorizer = load('vectorizerUdemy.joblib')

# Load the data
df = pd.read_csv('udemy_courses.csv')

# Preprocess the data
df.fillna('', inplace=True)  # fill missing values

# Function to recommend courses based on user input
def recommend_udemy(user_input):
    query = vectorizer.transform([user_input])
    distances, indices = model.kneighbors(query)
    valid_indices = [i for i in indices[0] if i < len(df)]
    recommendations = df.iloc[valid_indices]
    return recommendations

# Test the function
# print(recommend_udemy('python beginner'))