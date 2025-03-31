'''
    Provides the template for the tooltips.
'''

def age_distribution_hover(mode="Absolute"):
    label = "Count" if mode == "Absolute" else "Percentage"
    value = "%{marker.size:.1f}" if mode == "Relative" else "%{marker.size:.0f}"
    return (
        "Year: %{x}<br>"
        "Age Group Midpoint: %{y}<br>"
        f"{label}: {value}<extra></extra>"
    )
