from shiny import App, render, ui, reactive
from pandas import read_csv
from plotnine import ggplot, geom_point, geom_histogram, aes, theme_bw, scale_x_log10, scale_y_log10

app_ui = ui.page_fluid(
    ui.layout_sidebar(
        ui.panel_sidebar(
            ui.input_slider("sample", "Sample Size", 0, 1, value = 0.1),
            ui.input_checkbox("log", "Log Scale")
        ),
        ui.panel_main(
            ui.h3(ui.output_text("first_taxi_id")),
            ui.output_plot("tip_plot"),
            ui.output_plot("amount_histogram")
        )
    )
)

def server(input, output, session):
    @reactive.Calc
    def dat():
        import ssl
        ssl._create_default_https_context = ssl._create_unverified_context
        df = read_csv('nyc-taxi.csv')
        return df
    
    @reactive.Calc
    def sampled_dat():
        return dat().copy().sample(frac = input.sample())
    
    @output
    @render.text
    def first_taxi_id():
        return f'First taxi ID: {sampled_dat()["taxi_id"].iloc[0]}'

    @output
    @render.plot
    def tip_plot():
        plot = (ggplot(sampled_dat(), aes('tip_amount', 'total_amount'))
               + geom_point()
               + theme_bw()
               )
        if input.log():
            plot = (plot
                    + scale_x_log10()
                    + scale_y_log10())
        return plot
    
    @output
    @render.plot
    def amount_histogram():
        plot = (
            ggplot(sampled_dat(), aes(x='total_amount'))
            + geom_histogram()
            + theme_bw()
        )
        return plot

app = App(app_ui, server)