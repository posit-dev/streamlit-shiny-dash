"""Panel Reference Application with a focus on simplicity"""
import pandas as pd
import panel as pn

from plots import plot_hist, plot_tips


def first_taxi(data):
    if data.empty:
        return "First taxi id: None"
    return f'First taxi id: *{data["taxi_id"].iloc[0]}*'


pn.extension(
    sizing_mode="stretch_width",
)

accent = "#f7b731"

sample_input = pn.widgets.FloatSlider(
    value=0.1, start=0, end=1, step=0.01, name="Sample"
)
scale_input = pn.widgets.Checkbox(name="Use Log Scale", margin=(20, 10, 0, 10))

data = pn.state.as_cached(
    key="nyc-taxi", fn=pd.read_csv, filepath_or_buffer="nyc-taxi.csv"
)
plot_hist = pn.cache(plot_hist)
plot_tips = pn.cache(plot_tips)

sample_data = pn.bind(data.sample, frac=sample_input)

pn.template.FastListTemplate(
    site="Panel",
    title="NYC Taxi Data",
    sidebar=[
        "## NYC Taxi Data",
        sample_input,
        scale_input,
        pn.bind(first_taxi, sample_data),
    ],
    main=[
        pn.pane.Matplotlib(
            pn.bind(plot_tips, sample_data, scale_input, accent),
            max_height=500,
            sizing_mode="scale_both",
        ),
        pn.pane.Matplotlib(
            pn.bind(plot_hist, sample_data, accent),
            max_height=500,
            sizing_mode="scale_both",
        ),
    ],
    theme_toggle=False,
    accent=accent,
).servable()
