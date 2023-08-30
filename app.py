import shiny.experimental as x
import shinyswatch
from pandas import read_csv
from plotnine import (
    aes,
    geom_histogram,
    geom_point,
    ggplot,
    scale_x_log10,
    scale_y_log10,
    theme_bw,
)
from shiny import App, reactive, render, ui

app_ui = ui.page_fluid(
    shinyswatch.theme.minty(),
    ui.panel_title("Shiny"),
    x.ui.layout_sidebar(
        x.ui.sidebar(
            ui.input_slider("sample", "Sample Size", 0, 1, value=0.1, ticks=False),
            ui.input_checkbox("log", "Log Scale"),
        ),
        ui.panel_main(
            ui.h3(ui.output_text("first_taxi_id")),
            x.ui.card(x.ui.output_plot("tip_plot", fill=True)),
            x.ui.card(x.ui.output_plot("amount_histogram", fill=True)),
        ),
    ),
)


def server(input, output, session):
    @reactive.Calc
    def dat():
        df = read_csv("nyc-taxi.csv")
        return df

    @reactive.Calc
    def sampled_dat():
        return dat().sample(frac=input.sample())

    @output
    @render.text
    def first_taxi_id():
        return f'Sample ID: {sampled_dat()["taxi_id"].iloc[0]}'

    @output
    @render.plot
    def tip_plot():
        plot = (
            ggplot(sampled_dat(), aes("tip_amount", "total_amount"))
            + geom_point()
            + theme_bw()
        )
        if input.log():
            plot = plot + scale_x_log10() + scale_y_log10()
        return plot

    @output
    @render.plot
    def amount_histogram():
        plot = (
            ggplot(sampled_dat(), aes(x="total_amount"))
            + geom_histogram(binwidth=5)
            + theme_bw()
        )
        return plot


app = App(app_ui, server)
