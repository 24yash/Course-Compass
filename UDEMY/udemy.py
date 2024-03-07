import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import MinMaxScaler
from joblib import dump, load

# Load the data
df = pd.read_csv('udemy_courses.csv')

# Preprocess the data
df.fillna('', inplace=True)  # fill missing values

# Combine text features into one column
df['text'] = df['course_title'] + ' ' + df['level'] + ' ' + df['subject'] + ' ' + df['is_paid'].astype(str)

# Convert text into numerical vectors
vectorizer = TfidfVectorizer(stop_words='english')
X = vectorizer.fit_transform(df['text'])

# Scale the num_reviews to be between 0 and 1
scaler = MinMaxScaler()
df['num_reviews'] = scaler.fit_transform(df[['num_reviews']])

# Train a k-NN model
model = NearestNeighbors(n_neighbors=3, algorithm='ball_tree')
model.fit(X)

# Function to recommend courses based on user input
def recommend_courses(user_input):
    query = vectorizer.transform([user_input])
    distances, indices = model.kneighbors(query)
    recommendations = df.iloc[indices[0]]
    return recommendations.sort_values(by='num_reviews', ascending=False)

# Test the function
print(recommend_courses('python beginner'))

# Save the model and vectorizer
dump(model, 'modelUdemy.joblib')
dump(vectorizer, 'vectorizerUdemy.joblib')