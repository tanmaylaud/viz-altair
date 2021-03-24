import pandas as pd
import altair as alt
import numpy as np


def get_df():
    fatalities_df = pd.read_csv("./data/ukDriverFatalities.csv")
    return fatalities_df


def get_heatmap():
    fatalities_df = get_df()
    min_month, max_month = min(fatalities_df["month"]), max(fatalities_df["month"])
    min_year, max_year = min(fatalities_df["year"]), max(fatalities_df["year"])
    x, y = np.meshgrid(range(min_month, max_month + 1), range(min_year, max_year + 1))
    deaths = fatalities_df.pivot(
        index="month", columns="year", values="count"
    ).to_numpy()
    source = pd.DataFrame(
        {"month": x.ravel(), "year": y.ravel(), "deaths": deaths.ravel()}
    )
    return (
        alt.Chart(source, title="Deaths across time")
        .mark_rect()
        .encode(
            x=alt.X("month:O", scale=alt.Scale(zero=False)),
            y=alt.Y("year:O", scale=alt.Scale(zero=False)),
            color=alt.Color("deaths:Q"),
            tooltip=(["deaths"]),
        )
    )


def get_line_chart():
    return (
        alt.Chart(get_df(), title="Total deaths over the years")
        .mark_line(point=True)
        .encode(
            x="year",
            y=alt.Y("sum(count)", title="Total Deaths"),
            tooltip=([alt.Tooltip("sum(count)", title="Total Deaths")]),
        )
        .interactive(bind_y=False)
    )
