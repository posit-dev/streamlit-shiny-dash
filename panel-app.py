from pandas import read_csv
import panel as pn

from plots import plot_hist, plot_tips


def first_taxi(data):
    if data.empty:
        return '## First taxi id: *NA*'

    return f'## First taxi id: *{data["taxi_id"].iloc[0]}*'

pn.extension(
    sizing_mode="stretch_width",
)

data = pn.state.as_cached(
    key="nyc-taxi", fn=read_csv, filepath_or_buffer="nyc-taxi.csv"
)
plot_hist = pn.cache(plot_hist)
plot_tips = pn.cache(plot_tips)

sample_input = pn.widgets.FloatSlider(
    value=0.1, start=0, end=1, step=0.01, name="Sample"
)
scale_input = pn.widgets.Checkbox(name="Use Log Scale", margin=(20, 10, 0, 10))

sample_data = pn.bind(data.sample, frac=sample_input)

pn.template.FastListTemplate(
    site="Panel",
    title="NYC Taxi Data",
    sidebar=[
        "## NYC Taxi Data",
        sample_input,
        scale_input,
    ],
    main=[
        pn.bind(first_taxi, sample_data),
        pn.pane.Matplotlib(pn.bind(plot_tips, sample_data, scale_input), height=600),
        pn.pane.Matplotlib(pn.bind(plot_hist, sample_data), height=600  ),
    ],
    main_max_width="850px",
).servable()
