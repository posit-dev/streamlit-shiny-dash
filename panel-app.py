"""Panel Reference Application with a focus on simplicity"""
import pandas as pd
import panel as pn
import plotly.express as px


def first_taxi(data):
    return f'First taxi id: *{data["taxi_id"].iloc[0]}*'


def scatter_plot(data, scale, accent, template):
    use_log_scale = scale == "Log"
    fig = px.scatter(
        data,
        x="total_amount",
        y="tip_amount",
        log_x=use_log_scale,
        log_y=use_log_scale,
        color_discrete_sequence=[accent],
        template=template,
    )
    fig.update_layout(transition_duration=500, autosize=True)
    return fig


def histogram(data, accent, template):
    fig = px.histogram(
        data, x="total_amount", color_discrete_sequence=[accent], template=template
    )
    fig.update_layout(
        transition_duration=500,
        autosize=True,
    )
    return fig


CSS_FIX_SHOULD_BE_UPSTREAMED_TO_PANEL = """
.bk-active.bk-btn-primary {border-color: var(--accent-fill-active)}
.bk-btn-primary:hover {border-color: var(--accent-fill-hover)}
.bk-btn-primary {border-color: var(--accent-fill-rest)}
#sidebar {padding-left: 5px !important}
"""

pn.extension(
    "plotly",
    sizing_mode="stretch_width",
    raw_css=[CSS_FIX_SHOULD_BE_UPSTREAMED_TO_PANEL],
)

accent = "#f7b731"
plotly_template = "plotly_dark" if pn.config.theme == "dark" else "plotly"

sample_input = pn.widgets.FloatSlider(
    value=0.1, start=0, end=1, step=0.01, name="Sample"
)
scale_input = pn.widgets.RadioButtonGroup(
    options=["Linear", "Log"],
    button_type="primary",
    button_style="outline",
    name="Scale",
)

data = pn.state.as_cached(
    key="nyc-taxi", fn=pd.read_csv, filepath_or_buffer="nyc-taxi.csv"
)
rx_sample = pn.bind(data.sample, frac=sample_input)
rx_first_taxi = pn.bind(first_taxi, rx_sample)
rx_scatter_plot = pn.bind(scatter_plot, rx_sample, scale_input, accent, plotly_template)
rx_histogram = pn.bind(histogram, rx_sample, accent, plotly_template)

pn.template.FastListTemplate(
    site="Panel",
    title="NYC Taxi Data",
    sidebar=[
        "## NYC Taxi Data",
        pn.pane.Image("nyc-taxi.png", height=230),
        sample_input,
        "Scale: ",
        scale_input,
        rx_first_taxi,
    ],
    main=[rx_scatter_plot, rx_histogram],
    accent=accent,
).servable()
