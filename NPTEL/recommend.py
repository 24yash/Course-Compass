import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
from joblib import load

# Load the data
df = pd.read_csv('merged.csv')

# Load the model and vectorizer
model = load('modelNPTEL.joblib')
vectorizer = load('vectorizerNPTEL.joblib')

# Function to recommend courses based on user input
def recommend_nptel(user_input):
    query = vectorizer.transform([user_input])
    distances, indices = model.kneighbors(query)
    # recommendations = df.iloc[indices[0]][['Course ID', 'Course Name']]
    # recommendations = df.iloc[indices[0]]
    valid_indices = [i for i in indices[0] if i < len(df)]
    recommendations = df.iloc[valid_indices]
    return recommendations

# Test the function
# print(recommend_nptel('Hindi'))