import os
import numpy as np
import pandas as pd
from pycaret.classification import predict_model, load_model
import streamlit as st

model_dir = "/Users/USER/OneDrive - hull.ac.uk/AZURE/income/light_gbm_API"

# load the model
model = load_model(model_dir)

# create the streamlit app
st.title("Income Prediction app")

# create form for user input
st.sidebar.header("User Input Features")

df = pd.read_csv(r"C:\Users\USER\OneDrive - hull.ac.uk\AZURE\income\income.csv")


def clean_marital_status(status):
    married_list = ["Married-civ-spouse", "Married-AF-spouse"]
    if status in married_list:
        return "Married"
    else:
        return "Not_married"


df["marital-status"] = df["marital-status"].apply(lambda x: clean_marital_status(x))

# rename the target columns
df.rename(columns={"income >50K": "income"}, inplace=True)

# define the input features
features = df.drop("income", axis=1)
num_features = features.select_dtypes(include="number").columns.tolist()
cat_features = features.select_dtypes(include="object").columns.tolist()

input_fields = {}
for feature in num_features:
    input_fields[feature] = st.sidebar.slider(
        f"select {feature}", df[feature].min(), df[feature].max(), 0
    )

for feature in cat_features:
    input_fields[feature] = st.sidebar.selectbox(
        f"select {feature}", df[feature].unique()
    )

# create a dataframe for the user input
user_input = pd.DataFrame([input_fields])
income_group = ["<50K", ">50K"]

# make the prediction
if st.sidebar.button("predict"):
    prediction = predict_model(model, data=user_input, raw_score=True)
    st.write(prediction)
    predicted_label = prediction["prediction_label"].iloc[0]
    st.write(f"The predicted income group is: {income_group[predicted_label]}")
