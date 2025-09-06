import streamlit as st, pandas as pd, matplotlib.pyplot as plt

data = pd.read_csv("chat_logs.csv")

st.title("📊 Chatbot Analytics Dashboard")
st.write("User Query Trends")

st.bar_chart(data["intent"].value_counts())

sessions = data.groupby("user_id").size()
st.line_chart(sessions)
