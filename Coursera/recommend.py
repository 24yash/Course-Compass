from joblib import load
import pandas as pd
from sklearn.preprocessing import MinMaxScaler, LabelEncoder
from joblib import load

# Load the data
df = pd.read_csv('CourseraDataset.csv')

# Load the model and vectorizer
model = load('modelOLD.joblib')
vectorizer = load('vectorizerOLD.joblib')

# Use the model and vectorizer
def recommend_coursera(user_input):
    query = vectorizer.transform([user_input])
    distances, indices = model.kneighbors(query)
    recommendations = df.iloc[indices[0]]
    return recommendations.sort_values(by='Rating', ascending=False)

# print(recommend_coursera('money'))