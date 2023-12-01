from pandas import read_csv
from shiny import App, reactive, render, ui

from plots import plot_hist, plot_tips

app_ui = ui.page_sidebar(
    ui.sidebar(
        ui.input_slider("sample", "Sample Size", 0, 1, value=0.1, ticks=False),
        ui.input_checkbox("log", "Log Scale"),
    ),
    ui.h3(ui.output_text("first_taxi_id")),
    ui.card(ui.output_plot("tip_plot")),
    ui.card(ui.output_plot("amount_histogram")),
    title="Shiny",
)


def server(input, output, session):
    @reactive.Calc
    def dat():
        df = read_csv("nyc-taxi.csv")
        return df

    @reactive.Calc
    def sampled_dat():
        return dat().sample(frac=input.sample())

    @render.text
    def first_taxi_id():
        return f'Sample ID: {sampled_dat()["taxi_id"].iloc[0]}'

    @render.plot
    def tip_plot():
        return plot_tips(sampled_dat(), input.log())

    @output
    @render.plot
    def amount_histogram():
        return plot_hist(sampled_dat())


app = App(app_ui, server)
