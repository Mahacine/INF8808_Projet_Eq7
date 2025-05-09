from preprocess.preprocess import preprocess_sankey_data
import plotly.graph_objects as go

from style.theme import GOLD, SILVER, BRONZE, NO_MEDAL
import style.hover_template as hover_template

def create_sankey_plot(olympics_data, year, sport, selected_country, is_relative = False):
    '''
    Creates a Sankey plot to visualize the distribution of medals (Gold, Silver, Bronze, No Medal) 
    for a selected country and the top 3 countries in a selected sport

    args:
        olympics_data: The global dataframe
        year: The edition
        sport: The selected sport
        selected_country: The selected country
        is_relative: If True, percentages instead of counts

    returns:
        fig: The generated Sankey plot figure
        is_country_data_available: Boolean indicating whether the selected country's data is available
    '''

    # Preprocess data to get medal counts for the specified year, sport, and country
    df_medals, medal_counts = preprocess_sankey_data(olympics_data, year, sport, selected_country)
    
    if df_medals is None:
      return None, None

    # Get the list of countries and their corresponding names
    countries = medal_counts['NOC'].unique().tolist()
    countries_names = medal_counts['Region'].unique().tolist()

    # Add the nodes for medals ("Gold", "Silver", "Bronze", "No Medal") for each country
    all_labels = countries + [f'{medal}_{country}' for country in countries for medal in ['Gold', 'Silver', 'Bronze', 'No Medal']]

    # Indices mapping
    source_indices = []
    target_indices = []
    values = []

    medal_order = ['Gold', 'Silver', 'Bronze', 'No Medal']

    for country in countries:
        # Count the total number of medals
        medal_count = df_medals[(df_medals['NOC'] == country) & (df_medals['Medal'] != 'No Medal')].shape[0]

        medal_values = {medal: 0 for medal in medal_order}

        # Link each country and its medals
        for medal in ['Gold', 'Silver', 'Bronze']:

            medal_NOC = f'{medal}_{country}'

            if is_relative == False:
              count = medal_counts[(medal_counts['Medal_NOC'] == medal_NOC)]['Count'].sum()
            else:
              count = medal_counts[(medal_counts['Medal_NOC'] == medal_NOC)]['Percentage'].sum()
              medal_values[medal] = count

            source_indices.append(all_labels.index(country))
            target_indices.append(all_labels.index(medal_NOC))
            values.append(count)

        # Calculate the 'No Medal' count or percentage for the country
        if is_relative == False:
          no_medal_count = len(df_medals[df_medals['NOC'] == country]) - medal_count
        else:
          no_medal_count = 100 - sum(medal_values.values())

        no_medal_NOC = f'No Medal_{country}'
        source_indices.append(all_labels.index(country))
        target_indices.append(all_labels.index(no_medal_NOC))
        values.append(no_medal_count)

    # Define colors for each medal type
    medal_colors = {
        'Gold': GOLD, 
        'Silver': SILVER,
        'Bronze': BRONZE, 
        'No Medal': NO_MEDAL
    }

    # Assign 'black' for countries and 'red' to the selected country
    node_colors = ['black'] * len(countries)
    for idx, label in enumerate(countries):
      if label == selected_country:
          node_colors[idx] = 'red'

    # Assign colors for medal nodes based on medal type
    for label in all_labels:
        if 'Gold' in label:
            node_colors.append(medal_colors['Gold'])
        elif 'Silver' in label:
            node_colors.append(medal_colors['Silver'])
        elif 'Bronze' in label:
            node_colors.append(medal_colors['Bronze'])
        elif 'No Medal' in label:
            node_colors.append(medal_colors['No Medal'])

    # Assign link colors based on medal types
    link_colors = []
    for idx,color in enumerate(node_colors[len(countries):]):
       # Reference : https://www.30secondsofcode.org/python/s/hex-to-rgb/
       rgb = tuple(int(color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
       link_colors.append(f"rgba({rgb[0]}, {rgb[1]}, {rgb[2]}, 0.7)")
    
    # Create the Sankey plot
    fig = go.Figure(go.Sankey(
        orientation = 'v',
        arrangement = "snap",
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color='black', width=0.5),
            label = countries_names,
            color=node_colors,
            customdata=countries + [country for country in countries for _ in range(4)],
            hovertemplate=hover_template.source_sankey_hover(is_relative)
        ),
        link=dict(
            source=source_indices,
            target=target_indices,
            value=values,
            color=link_colors,
            line=dict(color="grey", width=0.3),
            customdata=[(label.split('_')[0], label.split('_')[1]) for label in all_labels if label not in countries],
            hovertemplate=hover_template.performance_sankey_hover(is_relative)
        )
    ))

    fig.update_layout(
        title_text=f'Edition : {year}',
        font_size=12
    )
    
    is_country_data_available = False
    if selected_country in countries:
      is_country_data_available = True

    return fig, is_country_data_available