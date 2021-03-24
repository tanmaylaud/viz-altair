import streamlit as st
from driverFatalities import get_df, get_heatmap, get_line_chart
from fluNet import get_line_chart, get_map
from studentScores import get_scatter, get_scatter_with_brush

assignment = st.sidebar.selectbox(
    "Assignment", ("Driver Fatalities", "Flu Net", "Student Scores")
)
if assignment == "Driver Fatalities":
    st.write("# Driver Fatalities")
    st.write(get_df().head().to_html(), unsafe_allow_html=True)
    if st.sidebar.checkbox("Show Heatmap", value=True):
        st.write(
            "## Heatmap showing the year in one axis, month in another, and the color should encode the number of deaths. Add legend."
        )
        st.altair_chart(get_heatmap(), use_container_width=True)
    if st.sidebar.checkbox("Show Line Chart", value=True):
        st.write("## Line chart showing the total number of deaths over the years.")
        st.altair_chart(get_line_chart(), use_container_width=True)

if assignment == "Flu Net":
    st.write("# Flu Net")
    st.altair_chart(get_line_chart(), use_container_width=True)
    st.altair_chart(get_line_chart(multi=True), use_container_width=True)
    st.altair_chart(get_map())

if assignment == "Student Scores":
    st.write("# Student Scores")
    st.altair_chart(get_scatter())
    st.altair_chart(get_scatter_with_brush())