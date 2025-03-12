import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Load the data
olympics_data = pd.read_csv('all_athlete_games.csv')

def main():
    # Header image
    st.image("header_image.png", use_container_width=True)

    # Sidebar for user inputs
    st.sidebar.title("User Inputs")
    st.sidebar.markdown("Please provide the following details:")
    user_name = st.sidebar.text_input("Enter your name")
    user_sex = st.sidebar.selectbox("Select your sex", ["Male", "Female"])
    discipline = st.sidebar.selectbox("Select a discipline", ["None"] + olympics_data["Sport"].unique().tolist())
    user_country = st.sidebar.selectbox("Select your country", ["None"] + olympics_data["NOC"].unique().tolist())

    # Filter data based on user inputs
    if discipline != "None" and user_country != "None":
        filtered_data = olympics_data[(olympics_data["Sport"] == discipline) & (olympics_data["Gender"] == user_sex) & (olympics_data["NOC"] == user_country)]
    elif discipline != "None":
        filtered_data = olympics_data[(olympics_data["Sport"] == discipline) & (olympics_data["Gender"] == user_sex)]
    elif user_country != "None":
        filtered_data = olympics_data[(olympics_data["Gender"] == user_sex) & (olympics_data["NOC"] == user_country)]
    else:
        filtered_data = olympics_data[olympics_data["Gender"] == user_sex]

    # Display user inputs
    st.write(f"Hello {user_name}!")
    st.write(f"You have selected {user_sex} athletes from {user_country if user_country != 'None' else 'all countries'} in {discipline if discipline != 'None' else 'all disciplines'}.")

    # Data visualization
    st.title("Olympics Data Exploration and Visualization")

    # Example visualization: Age Distribution of Athletes
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
                     title="Age Distribution of Athletes Over Time",
                     labels={"Year": "Year", "Age Group": "Age Group", "Count": "Number of Athletes"},
                     opacity=0.85,
                     size_max=40)

    # Update layout based on user's theme
    theme = st.get_option("theme.base")
    if theme == "dark":
        fig.update_layout(template="plotly_dark", font=dict(size=14), title_font=dict(size=18), plot_bgcolor="black", paper_bgcolor="black")
    else:
        fig.update_layout(template="simple_white", font=dict(size=14), title_font=dict(size=18), plot_bgcolor="white", paper_bgcolor="white")

    st.plotly_chart(fig)

    # Add more visualizations as needed based on the notebook content
    
    # Example visualization: Number of Athletes Over Time
    st.subheader("Number of Athletes Over Time")
    athletes_over_time = filtered_data.groupby("Year").size().reset_index(name="Count")
    fig = px.line(athletes_over_time,
                  x="Year",
                  y="Count",
                  title="Number of Athletes Over Time",
                  labels={"Year": "Year", "Count": "Number of Athletes"})
    st.plotly_chart(fig)

    # Example visualization: Age Distribution of Athletes scatter plot
    


    # Footer
    st.sidebar.markdown("---")
    st.sidebar.markdown("Developed by Team 7")
    st.sidebar.markdown("[GitHub Repository](https://github.com/Mahacine/INF8808_Projet_Eq7)")

if __name__ == "__main__":
    main()
