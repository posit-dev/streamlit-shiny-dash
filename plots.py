from matplotlib.pyplot import close
from plotnine import (
    aes,
    geom_histogram,
    geom_point,
    ggplot,
    scale_x_log10,
    scale_y_log10,
    theme_bw,
)


def plot_tips(sampled_data, log, color="black"):
    plot = (
        ggplot(sampled_data, aes("tip_amount", "total_amount"))
        + geom_point(color=color)
        + theme_bw()
    )
    if log:
        plot = plot + scale_x_log10() + scale_y_log10()
    fig = plot.draw()
    close()
    return fig


def plot_hist(sampled_data, color="black"):
    plot = (
        ggplot(sampled_data, aes(x="total_amount"))
        + geom_histogram(binwidth=5, color=color, fill=color)
        + theme_bw()
    )
    fig = plot.draw()
    close()
    return fig
