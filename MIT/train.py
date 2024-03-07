import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
from joblib import dump, load

# Load the data
df = pd.read_csv('mit.csv')

# Preprocess the data
df.fillna('', inplace=True)  # fill missing values

# Convert 'Course Title' into numerical vectors
vectorizer = TfidfVectorizer(stop_words='english')
X = vectorizer.fit_transform(df['Course Title'])

# Train a k-NN model
model = NearestNeighbors(n_neighbors=3, algorithm='ball_tree')
model.fit(X)

# Function to recommend courses based on user input
def recommend_courses(user_input):
    query = vectorizer.transform([user_input])
    distances, indices = model.kneighbors(query)
    recommendations = df.iloc[indices[0]]
    return recommendations

# Test the function
print(recommend_courses('engineering'))

# Save the model and vectorizer
dump(model, 'modelMIT.joblib')
dump(vectorizer, 'vectorizerMIT.joblib')