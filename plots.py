from plotnine import (
    aes,
    geom_histogram,
    geom_point,
    ggplot,
    scale_x_log10,
    scale_y_log10,
    theme_bw,
)


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
