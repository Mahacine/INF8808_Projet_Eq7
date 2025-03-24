import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Load the data
olympics_data = pd.read_csv('all_athlete_games.csv')

def main():
    # ---------------------------
    # Sidebar: User Inputs
    # ---------------------------
    st.sidebar.image("header_image.png", width=200)
    st.sidebar.title("Please provide the following details : ")
    user_sex = st.sidebar.selectbox("Select your sex", ["Male", "Female"])
    discipline = st.sidebar.selectbox("Select a discipline", ["None"] + olympics_data["Sport"].unique().tolist())
    user_country = st.sidebar.selectbox("Select your country", ["None"] + olympics_data["NOC"].unique().tolist())
    user_age = st.sidebar.text_input("Enter your age (0-99)")
    st.sidebar.markdown("---")
    st.sidebar.markdown("[![GitHub](https://img.icons8.com/ios-glyphs/30/ffffff/github.png)](https://github.com/Mahacine/INF8808_Projet_Eq7) Developed by Team 7 : ")
    st.sidebar.code("Rima Al Zawahra 2023119\nIman Bouara 1990495\nAlexis Desforges 2146454\nMahacine Ettahri 2312965\nNeda Khoshnoudi 2252125\nNicolas Lopez 2143179")

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

    # ---------------------------
    # Data Filtering
    # ---------------------------
    if discipline != "None" and user_country != "None":
        filtered_data = olympics_data[(olympics_data["Sport"] == discipline) & 
                                      (olympics_data["Gender"] == user_sex) & 
                                      (olympics_data["NOC"] == user_country)]
    elif discipline != "None":
        filtered_data = olympics_data[(olympics_data["Sport"] == discipline) & 
                                      (olympics_data["Gender"] == user_sex)]
    elif user_country != "None":
        filtered_data = olympics_data[(olympics_data["Gender"] == user_sex) & 
                                      (olympics_data["NOC"] == user_country)]
    else:
        filtered_data = olympics_data[olympics_data["Gender"] == user_sex]

    if user_age is not None:
        filtered_data = filtered_data[filtered_data["Age"] == user_age]

    st.title("Welcome to our Olympics Data Exploration and Visualization App")
    st.write(f"You have selected {user_sex} athletes from "
             f"{user_country if user_country != 'None' else 'all countries'} in "
             f"{discipline if discipline != 'None' else 'all disciplines'}.")

    # Define age bins, labels, and midpoints (used in several visualizations)
    age_bins = [10, 14, 17, 20, 23, 26, 30, 35, 100]
    age_labels = ["10-14", "15-17", "18-20", "21-23", "24-26", "27-30", "31-35", "36+"]
    age_midpoints = {"10-14": 12, "15-17": 16, "18-20": 19, "21-23": 22, 
                     "24-26": 25, "27-30": 28, "31-35": 33, "36+": 40}

    # ===========================
    # Visualization 1
    # Q1: Quel est l'âge moyen des athlètes dans ma discipline et comment a-t-il évolué au fil du temps ?
    # Q2: Quelle est la répartition de chaque catégorie d'âge ?
    # ===========================
    st.subheader("Visualization 1: Quel est l'âge moyen des athlètes dans ma discipline et comment a-t-il évolué au fil du temps et quelle est la répartition de chaque catégorie d'âge ?")
    # Interactive controls: absolute vs relative and option to overlay average age
    mode = st.radio("Select mode for bubble size", ("Absolute", "Relative"), key="mode_age_distribution")
    show_avg = st.checkbox("Show Average Age", key="show_avg_age")

    # Prepare data for visualization 1
    data_plot = filtered_data.copy().dropna(subset=["Age"])
    data_plot["Age Group"] = pd.cut(data_plot["Age"], bins=age_bins, labels=age_labels, right=False)
    data_plot["Age_Midpoint"] = data_plot["Age Group"].map(age_midpoints)
    grouped = data_plot.groupby(["Year", "Age Group"]).size().reset_index(name="Count")
    grouped["Age_Midpoint"] = grouped["Age Group"].map(age_midpoints)

    if mode == "Relative":
        total_per_year = grouped.groupby("Year")["Count"].transform("sum")
        grouped["Percentage"] = (grouped["Count"] / total_per_year) * 100
        size_column = "Percentage"
    else:
        size_column = "Count"

    if show_avg:
        fig1 = make_subplots(specs=[[{"secondary_y": True}]])
    else:
        fig1 = go.Figure()

    fig1.add_trace(
        go.Scatter(
            x=grouped["Year"],
            y=grouped["Age_Midpoint"],
            mode="markers",
            marker=dict(
                size=grouped[size_column],
                sizemode="area",
                sizeref=2.*max(grouped[size_column])/(40.**2),
                sizemin=4,
                color=grouped["Age_Midpoint"],
                colorscale="Viridis",
                showscale=True,
            ),
            text=grouped["Age Group"].astype(str) + "<br>" + size_column + ": " + grouped[size_column].round(1).astype(str),
            hovertemplate="Year: %{x}<br>Age Group: %{text}<extra></extra>",
        ),
        secondary_y=False if show_avg else None
    )

    if show_avg:
        avg_age = data_plot.groupby("Year")["Age"].mean().reset_index(name="Average Age")
        fig1.add_trace(
            go.Scatter(
                x=avg_age["Year"],
                y=avg_age["Average Age"],
                mode="lines+markers",
                name="Average Age",
                line=dict(color="red"),
            ),
            secondary_y=True
        )
        fig1.update_yaxes(title_text="Age Group (Midpoint)", secondary_y=False,
                          tickvals=list(age_midpoints.values()), ticktext=list(age_midpoints.keys()))
        fig1.update_yaxes(title_text="Average Age", secondary_y=True)
    else:
        fig1.update_yaxes(title_text="Age Group (Midpoint)",
                          tickvals=list(age_midpoints.values()), ticktext=list(age_midpoints.keys()))

    fig1.update_layout(
        title="Evolution of Age Distribution and Average Age Over Time",
        xaxis_title="Year",
        legend_title="Legend"
    )
    st.plotly_chart(fig1)

    # ===========================
    # Visualization 2
    # Q4: Comment l'âge des athlètes évolue-t-il selon les sous-catégories de ma discipline ?
    # ===========================
    st.subheader("Visualisation 2: Comment l'âge des athlètes évolue-t-il selon les sous-catégories de ma discipline ?")
    if discipline != "None":
        events = filtered_data["Event"].unique().tolist()
        event_selected = st.selectbox("Select a sub-category (Event)", ["All"] + events, key="event_select")
        if event_selected != "All":
            data_event = filtered_data[filtered_data["Event"] == event_selected].copy()
        else:
            data_event = filtered_data.copy()
        data_event = data_event.dropna(subset=["Age"])
        data_event["Age Group"] = pd.cut(data_event["Age"], bins=age_bins, labels=age_labels, right=False)
        data_event["Age_Midpoint"] = data_event["Age Group"].map(age_midpoints)
        grouped_event = data_event.groupby(["Year", "Age Group"]).size().reset_index(name="Count")
        grouped_event["Age_Midpoint"] = grouped_event["Age Group"].map(age_midpoints)
        mode_event = st.radio("Select mode (Event)", ("Absolute", "Relative"), key="mode_event")
        if mode_event == "Relative":
            total_event = grouped_event.groupby("Year")["Count"].transform("sum")
            grouped_event["Percentage"] = (grouped_event["Count"] / total_event) * 100
            size_col_event = "Percentage"
        else:
            size_col_event = "Count"
        fig2 = px.scatter(grouped_event,
                          x="Year",
                          y="Age_Midpoint",
                          size=size_col_event,
                          color="Age Group",
                          labels={"Year": "Year", "Age Group": "Age Group", size_col_event: "Count/Percentage"},
                          opacity=0.85,
                          size_max=40)
        fig2.update_yaxes(tickvals=list(age_midpoints.values()), ticktext=list(age_midpoints.keys()),
                          title="Age Group (Midpoint)")
        st.plotly_chart(fig2)
    else:
        st.info("Please select a discipline to view sub-category analysis.")

    # ===========================
    # Visualization 3
    # Q3: Existe-t-il une tranche d'âge optimale pour remporter une médaille dans ma discipline ?
    # ===========================
    st.subheader("Visualisation 3: Existe-t-il une tranche d'âge optimale pour remporter une médaille dans ma discipline ?")
    if discipline != "None":
        data_medal = filtered_data[filtered_data["Medal"] != "No medal"].copy()
        if not data_medal.empty:
            data_medal["Age Group"] = pd.cut(data_medal["Age"], bins=age_bins, labels=age_labels, right=False)
            medal_group = data_medal.groupby(["Medal", "Age Group"]).size().reset_index(name="Count")
            medal_group["Age_Midpoint"] = medal_group["Age Group"].map(age_midpoints)
            fig3 = px.scatter(medal_group,
                              x="Medal",
                              y="Age_Midpoint",
                              size="Count",
                              color="Age Group",
                              labels={"Medal": "Medal Type", "Age_Midpoint": "Age Group (Midpoint)", "Count": "Number of Medalists"},
                              size_max=40,
                              opacity=0.8)
            fig3.update_yaxes(tickvals=list(age_midpoints.values()), ticktext=list(age_midpoints.keys()),
                              title="Age Group")
            st.plotly_chart(fig3)
        else:
            st.info("No medal data available for the selected filters.")
    else:
        st.info("Please select a discipline to view medal analysis.")

    # ===========================
    # Visualization 4
    # Q5, Q6 & Q7: Analyse de la performance et de la participation par pays via un diagramme Sankey
    # ===========================
    st.subheader("Visualisation 4: Comment mon pays a-t-il performé historiquement et comparativement aux pays de référence ?")
    if user_country != "None":
        if discipline != "None":
            data_country = olympics_data[(olympics_data["Sport"] == discipline) & (olympics_data["Gender"] == user_sex)].copy()
        else:
            data_country = olympics_data[olympics_data["Gender"] == user_sex].copy()
        country_medals = data_country.groupby(["NOC", "Medal"]).size().reset_index(name="Count")
        country_counts = data_country.groupby("NOC").size().reset_index(name="Total")
        country_perf = pd.merge(country_medals, country_counts, on="NOC")
        top_countries = country_counts.sort_values("Total", ascending=False)["NOC"].unique()[:3].tolist()
        if user_country not in top_countries:
            selected_countries = top_countries + [user_country]
        else:
            selected_countries = top_countries
        sankey_data = country_perf[country_perf["NOC"].isin(selected_countries)]
        medal_categories = ["No medal", "Gold", "Silver", "Bronze"]
        node_labels = list(selected_countries) + medal_categories
        node_dict = {label: idx for idx, label in enumerate(node_labels)}
        sankey_links = sankey_data[sankey_data["Medal"].isin(medal_categories)]
        sources = sankey_links["NOC"].map(node_dict).tolist()
        targets = sankey_links["Medal"].map(lambda x: node_dict[x]).tolist()
        values = sankey_links["Count"].tolist()
        node_colors = []
        for label in node_labels:
            if label == user_country:
                node_colors.append("red")
            else:
                node_colors.append("blue" if label in selected_countries else "gray")
        fig4 = go.Figure(data=[go.Sankey(
            node = dict(
                pad = 15,
                thickness = 20,
                line = dict(color = "black", width = 0.5),
                label = node_labels,
                color = node_colors
            ),
            link = dict(
                source = sources,
                target = targets,
                value = values,
                hovertemplate="Source: %{source.label}<br>Target: %{target.label}<br>Value: %{value}<extra></extra>"
            )
        )])
        fig4.update_layout(title_text="Country Participation and Medal Distribution", font_size=10)
        st.plotly_chart(fig4)
    else:
        st.info("Please select a country to view performance analysis.")

    # ===========================
    # Visualization 5
    # Q8: Pour ma discipline, existe-t-il des disparités entre hommes et femmes ?
    # ===========================
    st.subheader("Visualisation 5: Pour ma discipline, existe-t-il des disparités entre hommes et femmes ?")
    if discipline != "None":
        gender_data = olympics_data[(olympics_data["Sport"] == discipline)].copy()
        gender_counts = gender_data.groupby(["Event", "Gender"]).size().reset_index(name="Count")
        gender_pivot = gender_counts.pivot(index="Event", columns="Gender", values="Count").dropna().reset_index()
        gender_pivot = gender_pivot.sort_values("Male", ascending=False)
        fig5 = go.Figure()
        fig5.add_trace(go.Scatter(
            x=gender_pivot["Male"],
            y=gender_pivot["Event"],
            mode="markers",
            marker=dict(color="blue", size=10),
            name="Male"
        ))
        fig5.add_trace(go.Scatter(
            x=gender_pivot["Female"],
            y=gender_pivot["Event"],
            mode="markers",
            marker=dict(color="pink", size=10),
            name="Female"
        ))
        for i, row in gender_pivot.iterrows():
            fig5.add_trace(go.Scatter(
                x=[row["Male"], row["Female"]],
                y=[row["Event"], row["Event"]],
                mode="lines",
                line=dict(color="gray"),
                showlegend=False
            ))
        fig5.update_layout(
            xaxis_title="Number of Participants",
            yaxis_title="Event",
            title="Gender Disparities in Participation for " + discipline,
            height=600
        )
        st.plotly_chart(fig5)
    else:
        st.info("Please select a discipline to view gender disparities.")

    # ===========================
    # Visualization 6
    # Q9 & Q10: Évolution de la répartition hommes-femmes et participation féminine dans le temps
    # ===========================
    st.subheader("Visualisation 6: Evolution of Gender Participation Over Time")
    if discipline != "None":
        data_gender = olympics_data[(olympics_data["Sport"] == discipline) & 
                                    (olympics_data["Gender"].isin(["Male", "Female"]))].copy()
    else:
        data_gender = olympics_data[olympics_data["Gender"].isin(["Male", "Female"])].copy()
    gender_year = data_gender.groupby(["Year", "Gender"]).size().reset_index(name="Count")
    year_totals = gender_year.groupby("Year")["Count"].transform("sum")
    gender_year["Percentage"] = (gender_year["Count"] / year_totals) * 100
    fig6 = px.bar(gender_year, x="Year", y="Percentage", color="Gender", barmode="stack",
                  labels={"Percentage": "Percentage of Participants", "Year": "Year"},
                  title="Gender Participation Over Time",
                  color_discrete_map={"Male": "blue", "Female": "pink"})
    fig6.add_hline(y=50, line_dash="dash", line_color="black")
    st.plotly_chart(fig6)

    # ===========================
    # Visualization 7
    # Q11: Combien de participations un athlète dans ma discipline a-t-il généralement avant de remporter une médaille ?
    # ===========================
    st.subheader("Visualisation 7: Nombre de participations avant de remporter une médaille")
    if discipline != "None":
        data_sorted = filtered_data.sort_values(["Name", "Year"]).copy()
        data_sorted["Participation"] = data_sorted.groupby("Name").cumcount() + 1
        data_medal_first = data_sorted[data_sorted["Medal"] != "No medal"].groupby("Name").first().reset_index()
        if not data_medal_first.empty:
            medal_first_group = data_medal_first.groupby(["Participation", "Medal"]).size().reset_index(name="MedalCount")
            participation_counts = data_sorted.groupby("Name")["Participation"].max().reset_index()
            def athletes_with_min_participation(n):
                return (participation_counts["Participation"] >= n).sum()
            medal_first_group["Percentage"] = medal_first_group.apply(
                lambda row: (row["MedalCount"] / athletes_with_min_participation(row["Participation"])) * 100, axis=1)
            fig7 = px.bar(medal_first_group, x="Participation", y="Percentage", color="Medal",
                          labels={"Participation": "Participation Order", "Percentage": "Percentage of Medal Winners"},
                          title="Chances d'obtenir une médaille par ordre de participation")
            st.plotly_chart(fig7)
        else:
            st.info("No medal data available for the selected filters.")
    else:
        st.info("Please select a discipline to view medal participation analysis.")

    # ===========================
    # Visualization 8
    # Q12: Combien de fois pourrais-je participer aux Jeux Olympiques tout au long de ma carrière ?
    # ===========================
    st.subheader("Visualisation 8: Career Participation Span Across Sports")
    career_data = olympics_data.groupby("Sport")["Age"].agg(Min_Age="min", Max_Age="max").reset_index()
    fig8 = go.Figure()
    for i, row in career_data.iterrows():
        color = "red" if (discipline != "None" and row["Sport"] == discipline) else "blue"
        fig8.add_trace(go.Scatter(
            x=[row["Sport"], row["Sport"]],
            y=[row["Min_Age"], row["Max_Age"]],
            mode="lines+markers",
            line=dict(dash="dot", color=color),
            marker=dict(size=10, color=color),
            showlegend=False
        ))
    fig8.update_layout(
        xaxis_title="Sport",
        yaxis_title="Age",
        title="Career Participation Span by Sport",
        xaxis_tickangle=-45
    )
    st.plotly_chart(fig8)

if __name__ == "__main__":
    main()
