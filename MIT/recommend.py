import pandas as pd
from joblib import load

# Load the data
df = pd.read_csv('mit.csv')

# Load the model and vectorizer
model = load('modelMIT.joblib')
vectorizer = load('vectorizerMIT.joblib')

# Use the model and vectorizer
def recommend_mit(user_input):
    query = vectorizer.transform([user_input])
    distances, indices = model.kneighbors(query)
    recommendations = df.iloc[indices[0]]
    return recommendations

# Test the function
# print(recommend_mit('history'))