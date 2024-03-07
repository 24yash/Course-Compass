import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
from joblib import dump

# Load the data
df = pd.read_csv('merged.csv')

# Fill missing values
for col in df.columns:
    if df[col].dtype == 'object' or df[col].dtype == 'int64':
        df[col] = df[col].fillna('')
    else:
        df[col] = df[col].fillna(0)  # or use df[col].mean()

# # Combine text features into one column
df['text'] = df['Discipline'] + ' ' + df['Course Name'] + ' ' + df['SME Name'] + ' ' + df['Institute'] + ' ' + df['Co-ordinating Institute'] + ' ' + df['Duration'] + ' ' + df['Type of course'] + ' ' + df['UG/PG'] + ' ' + df['Core/Elective']
df['text'] = df['text'].astype(str)
# Combine only the most relevant text features into one column
# df['text'] = df['Course Name'] + ' ' + df['Discipline']
# df['text'] = df['text'].astype(str)

# Remove rows where 'text' is empty or contains only whitespace
df = df[df['text'].str.strip() != '']

# Convert text into numerical vectors
vectorizer = TfidfVectorizer(stop_words='english')
X = vectorizer.fit_transform(df['text']).toarray()  # convert to dense matrix

# Train a k-NN model
model = NearestNeighbors(n_neighbors=3, algorithm='brute')  # use brute algorithm
model.fit(X)

# Function to recommend courses based on user input
def recommend_courses(user_input):
    query = vectorizer.transform([user_input])
    distances, indices = model.kneighbors(query)
    recommendations = df.iloc[indices[0]][['Course ID', 'Course Name']]
    return recommendations

# Test the function
print(recommend_courses('Mathematics'))

# Save the model and vectorizer
dump(model, 'modelNPTEL.joblib')
dump(vectorizer, 'vectorizerNPTEL.joblib')