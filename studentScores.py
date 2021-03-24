import pandas as pd
import altair as alt


def get_df():
    college_scores_df = pd.read_csv("./data/calvinCollegeSeniorScores.csv")
    return college_scores_df


def get_scatter():
    return (
        alt.Chart(get_df())
        .mark_point(filled=True, opacity=0.3)
        .encode(
            x="SATM",
            y="SATV",
            color="GPA",
            size="ACT",
            tooltip=(["SATM", "SATV", "GPA", "ACT"]),
        )
        .interactive()
    )


def get_scatter_with_brush():
    brush = alt.selection_interval()
    color_condition = alt.condition(brush, "GPA", alt.value("lightgray"))
    college_scores_df = get_df()
    plot_1 = (
        alt.Chart(college_scores_df, title="SATM vs SATV")
        .mark_point(filled=True)
        .encode(x="SATM", y="SATV", color=color_condition, tooltip=(["SATM", "SATV"]))
        .add_selection(brush)
    )

    plot_2 = (
        alt.Chart(college_scores_df, title="ACT vs GPA")
        .mark_point(filled=True)
        .encode(x="ACT", y="GPA", color=color_condition, tooltip=(["ACT", "GPA"]))
        .add_selection(brush)
    )

    return plot_1 | plot_2