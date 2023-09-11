import streamlit as st
import pandas as pd
from sklearn import datasets
from sklearn.ensemble import RandomForestClassifier

st.markdown("""
# Simple Iris Flower Prediction app

This app predicts the iris flower type
""")
            
st.sidebar.header('User Input Parameters')
uploaded_file = st.sidebar.file_uploader("Upload your input CSV file", type=["xls"])

def user_input_features():
    sepal_length = st.sidebar.slider('Sepal Length', 4.3, 7.9, 5.4)
    sepal_width = st.sidebar.slider('Sepal width', 2.0, 4.4, 3.4)
    petal_length = st.sidebar.slider('Petal length', 1.0, 6.9, 1.3)
    petal_width = st.sidebar.slider('Petal width', 0.1, 2.5, 0.2)

    data = {
        "sepal_length" : sepal_length,
        'sepal width': sepal_width,
        'petal length' : petal_length,
        'petal width' : petal_width
    }

    features = pd.DataFrame(data, index=[0])
    return features
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    del df['species']
    df = df.sample(frac=1)

else:
    df = user_input_features()
st.subheader('User Input parameters')
st.write(df)

iris = datasets.load_iris()
X = iris.data
Y = iris.target

classifier = RandomForestClassifier()
classifier.fit(X, Y)

prediction = classifier.predict(df)
prediction_prob = classifier.predict_proba(df)

st.subheader('Class labels and their corresponding index numbers')
abc = pd.DataFrame(iris.target_names)
abc.reset_index()
abc.rename(columns = {0: "targets"}, inplace=True)
st.write(abc)
# target = []
# index = []
# for i,j in enumerate(iris.target_names):
#     target.append(i)
#     index.append(j)
# data = pd.DataFrame(index,target)
# abc.rename(columns = {0: "targets"}, inplace=True)
# st.write(data)

st.subheader('Prediction')
st.write(iris.target_names[prediction])

st.subheader('Prediction Probability')
st.write(prediction_prob)