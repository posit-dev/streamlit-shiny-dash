import time

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

import gradio as gr

taxi = read_csv("nyc-taxi.csv")


def sample_data(slider):
    time.sleep(1)
    out = taxi.sample(frac=slider)

    return {sampled_data: out}


def plot_tips(sampled_data, log):
    plot = (
        ggplot(sampled_data, aes("tip_amount", "total_amount"))
        + geom_point()
        + theme_bw()
    )
    if log:
        plot = plot + scale_x_log10() + scale_y_log10()
    return plot.draw()


def plot_hist(sampled_data):
    plot = (
        ggplot(sampled_data, aes(x="total_amount"))
        + geom_histogram(binwidth=5)
        + theme_bw()
    )
    return plot.draw()


with gr.Blocks() as demo:
    sampled_data = gr.State(None)
    with gr.Row():
        with gr.Column(scale=2):
            slider = gr.Slider(0, 1, value=0.1, step=0.01)
            log_scale = gr.Checkbox(label="Log Scale")

        with gr.Column(scale=10):
            tip_plot = gr.Plot()
            hist_plot = gr.Plot()

    slider.change(sample_data, [slider], [sampled_data]).then(
        plot_tips, [sampled_data, log_scale], [tip_plot]
    ).then(plot_hist, [sampled_data], [hist_plot])

    log_scale.change(plot_tips, [sampled_data, log_scale], [tip_plot])


if __name__ == "__main__":
    demo.launch()
