import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Load the data
olympics_data = pd.read_csv('all_athlete_games.csv')

def main():

    # Sidebar
    st.sidebar.image("header_image.png", width=200)
    st.sidebar.title("Please provide the following details : ")
    user_sex = st.sidebar.selectbox("Select your sex", ["Male", "Female"])
    discipline = st.sidebar.selectbox("Select a discipline", ["None"] + olympics_data["Sport"].unique().tolist())
    user_country = st.sidebar.selectbox("Select your country", ["None"] + olympics_data["NOC"].unique().tolist())
    user_age = st.sidebar.text_input("Enter your age (0-99)")
    st.sidebar.markdown("---")
    st.sidebar.markdown("Developed by Team 7 : ")
    st.sidebar.code("Rima Al Zawahra 2023119\nIman Bouara 1990495\nAlexis Desforges 2146454\nMahacine Ettahri 2312965 \nNeda Khoshnoudi 2252125\nNicolas Lopez 2143179")
    st.sidebar.markdown("[![GitHub](https://img.icons8.com/ios-glyphs/30/000000/github.png)](https://github.com/Mahacine/INF8808_Projet_Eq7)")

    

    # Validate age input
    if user_age:
        if user_age.isdigit():
            user_age = int(user_age)
            if user_age < 0 or user_age > 99:
                st.sidebar.error("Age must be between 0 and 99.")
                return
        else:
            st.sidebar.error("Please enter a valid age.")
            return
    else:
        user_age = None

    # Filter data based on user inputs
    if discipline != "None" and user_country != "None":
        filtered_data = olympics_data[(olympics_data["Sport"] == discipline) & (olympics_data["Gender"] == user_sex) & (olympics_data["NOC"] == user_country)]
    elif discipline != "None":
        filtered_data = olympics_data[(olympics_data["Sport"] == discipline) & (olympics_data["Gender"] == user_sex)]
    elif user_country != "None":
        filtered_data = olympics_data[(olympics_data["Gender"] == user_sex) & (olympics_data["NOC"] == user_country)]
    else:
        filtered_data = olympics_data[olympics_data["Gender"] == user_sex]

    if user_age is not None:
        filtered_data = filtered_data[filtered_data["Age"] == user_age]


    # Data visualization
    st.title("Welcome to our Olympics Data Exploration and Visualization App")
    st.write(f"You have selected {user_sex} athletes from {user_country if user_country != 'None' else 'all countries'} in {discipline if discipline != 'None' else 'all disciplines'}.")



    # Visualization: Age Distribution of Athletes
    st.subheader("Age Distribution of Athletes")
    age_bins = [10, 14, 17, 20, 23, 26, 30, 35, 100]
    age_labels = ["10-14", "15-17", "18-20", "21-23", "24-26", "27-30", "31-35", "36+"]
    filtered_data["Age Group"] = pd.cut(filtered_data["Age"], bins=age_bins, labels=age_labels, right=False)
    age_grouped = filtered_data.groupby(["Year", "Age Group"]).size().reset_index(name="Count")

    fig = px.scatter(age_grouped,
                     x="Year",
                     y="Age Group",
                     size="Count",
                     color="Age Group",
                     labels={"Year": "Year", "Age Group": "Age Group", "Count": "Number of Athletes"},
                     opacity=0.85,
                     size_max=40)

    st.plotly_chart(fig)

    
    # Visualization: Number of Athletes Over Time
    st.subheader("Number of Athletes Over Time")
    athletes_over_time = filtered_data.groupby("Year").size().reset_index(name="Count")
    fig = px.line(athletes_over_time,
                  x="Year",
                  y="Count",
                  labels={"Year": "Year", "Count": "Number of Athletes"})
    st.plotly_chart(fig)



if __name__ == "__main__":
    main()
