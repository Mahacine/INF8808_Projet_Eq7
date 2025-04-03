# import plotly.express as px

# def visualize_data(data):
#     fig = px.bar(
#         data,
#         x="Year",
#         y=["Female %", "Male %"],
#         labels={"value": "Percentage of Athletes", "Year": "Olympic Year"},
#         title="Evolution of Male and Female Participation in Olympic Athletics",
#         color_discrete_map={"Female %": "pink", "Male %": "blue"}
#     )

#     fig.update_layout(
#         barmode="relative",
#         xaxis=dict(
#             type="category",
#             tickmode="array",
#             tickvals=data["Year"],
#             ticktext=data["Year"],
#         ),
#         yaxis=dict(title="% Share of Athletes"),
#         plot_bgcolor="white"
#     )

#     fig.add_hline(y=50, line_dash="dash", line_color="black", annotation_text="50%",
#                   annotation_position="right", annotation_font_size=14, annotation_font_color="black")

#     fig.update_xaxes(tickangle=-90)

#     fig.show()

import plotly.express as px


def visualize_data(data, sport):
    fig = px.bar(
        data,
        x="Year",
        y=["Female %", "Male %"],
        labels={"value": "Percentage of Athletes", "Year": "Olympic Year"},
        title=f"Evolution of Male and Female Participation in {sport}",
        color_discrete_map={"Female %": "pink", "Male %": "blue"}
        symbol="Gender percentage"
    )

    fig.update_layout(
        barmode="relative",
        xaxis=dict(
            type="category",
            tickmode="array",
            tickvals=data["Year"],
            ticktext=data["Year"],
        ),
        yaxis=dict(title="percentage of participation"),
        plot_bgcolor="white"
    )

    fig.add_hline(y=50, line_dash="dash", line_color="black", annotation_text="50%",
                  annotation_position="right", annotation_font_size=14, annotation_font_color="black")

    fig.update_xaxes(tickangle=-90)

    return fig
