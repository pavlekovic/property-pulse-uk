import altair as alt
import pandas as pd

def price_lines(df: pd.DataFrame, name_col: str = "district"):
    """Create a line chart of average property prices over time by district."""
    
    # nearest selection on x (year)
    nearest = alt.selection_point(encodings=["x"], nearest=True, empty=False, on="pointermove")
    
    base = (
        alt
        .Chart(df)
        #.mark_line(interpolate="monotone", strokeWidth=3)
        .encode(
            x=alt.X("year:O", title="Year", axis=alt.Axis(labelAngle=0)),
            y=alt.Y("avg_price:Q", title="Average Price (£)"),
            color=alt.Color(f"{name_col}:N", title="District"),
            #tooltip=[name_col, "year", alt.Tooltip("avg_price:Q", format=",.0f")]
        )
        .properties(height=600)
    )
    
    lines = base.mark_line(interpolate="monotone", strokeWidth=3)
    
    # transparent selectors to drive the hover
    selectors = alt.Chart(df).mark_rule(opacity=0).encode(x="year:O").add_params(nearest)

    # highlight the nearest points
    points = base.mark_circle(size=100).encode(
        opacity=alt.condition(nearest, alt.value(1), alt.value(0))
    )

    text = base.mark_text(align="left", dx=10, dy=15, size=16).encode(
        text=alt.condition(nearest, alt.Text("avg_price:Q", format=",.0f"), alt.value(""))
    )
    
    # vertical rule at the hovered year
    rule = alt.Chart(df).mark_rule(strokeDash=[4, 4]).encode(
        x="year:O", opacity=alt.condition(nearest, alt.value(1), alt.value(0))
    )
    
    # shaded band: 2008 → 2009
    band = (
        alt.Chart(pd.DataFrame({"start": ["2008"], "end": ["2009"]}))
        .mark_rect(color="red", opacity=0.12)
        .encode(x="start:O", x2="end:O")
    )
    
    return alt.layer(lines, selectors, points, text, rule)

