import pandas as pd
import altair as alt
from vega_datasets import data


def plot(selection, transformed_df):
    """"""
    color = alt.condition(
        selection, alt.Color("country:N", legend=None), alt.value("lightgray")
    )

    base = alt.Chart(transformed_df, title="Flu cases per week").encode(
        x=alt.X("week:Q", title="Week"),
        y=alt.Y("flu_cases:Q", title="Flu Cases"),
        color=color,
        tooltip=([alt.Tooltip("flu_cases:Q", title="Total Cases")]),
    )

    line = base.mark_line().add_selection(selection).interactive(bind_y=False)

    return line, color


def get_df():
    flunet_df = pd.read_csv("./data/flunet2010_11countries_106.csv")
    return flunet_df


def get_line_chart(multi=False):
    flunet_df = get_df()
    countries = flunet_df.columns.tolist()[1:]
    transformed_df = pd.melt(
        flunet_df,
        id_vars=["week"],
        value_vars=countries,
        var_name="country",
        value_name="flu_cases",
    )
    transformed_df["index"] = transformed_df["week"] % 53
    slider1 = alt.binding_range(min=1, max=52, step=1)
    slider2 = alt.binding_range(min=1, max=52, step=1)
    select_week1 = alt.selection_single(name="week1", fields=["week"], bind=slider1)
    select_week2 = alt.selection_single(name="week2", fields=["week"], bind=slider2)
    if multi:
        multi_select = alt.selection_multi(fields=["country"])
        selection = alt.selection_multi(fields=["country"])
        line, color = plot(selection, transformed_df)
        make_selector = (
            alt.Chart(pd.DataFrame({"country": countries}))
            .mark_rect()
            .encode(y="country", color=color)
            .add_selection(selection)
        )
        return line | make_selector
    selector = alt.selection(
        type="single",
        fields=["country"],
        bind=alt.binding_select(options=countries),
        name="Select",
    )

    line, _ = plot(selector, transformed_df)
    return (
        line.add_selection(select_week2)
        .add_selection(select_week1)
        .transform_filter("datum.week > week1_week")
        .transform_filter("datum.week < week2_week")
    )


def get_map():
    country_data = pd.read_csv("./data/countries.csv")
    countries = get_df().columns.tolist()[1:]
    name_id = country_data[country_data["name"].isin(countries)][["name", "id"]]
    choropleth_df = (
        name_id.reset_index(drop=True)
        .merge(pd.DataFrame(get_df().sum().T), left_on="name", right_index=True)
        .rename(columns={0: "flu_cases"})
    )
    source = alt.topo_feature(data.world_110m.url, "countries")
    background = (
        alt.Chart(source)
        .mark_geoshape(fill="lightgray", stroke="white")
        .project("equirectangular")
    )
    choropleth = (
        alt.Chart(source)
        .mark_geoshape(stroke="white")
        .transform_lookup(
            lookup="id",
            from_=alt.LookupData(choropleth_df, "id", list(choropleth_df.columns)[2:]),
        )
        .encode(
            color="flu_cases:Q",
            tooltip=([alt.Tooltip("flu_cases:Q", title="Total Cases")]),
        )
        .properties(width=500, height=300, title="Annual Net Flu Cases")
        .project("equirectangular")
    )
    return background + choropleth
