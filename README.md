# Data App Comparison

This repo illustrates some differences between

- [Dash](https://plotly.com/dash/)
- [Panel](https://panel.holoviz.org/reference/index.html)
- [Shiny for Python](https://shiny.posit.co/)
- [Shiny for R](https://shiny.posit.co/)
- [Streamlit](https://streamlit.io/)

To get started set up a virtual environment and install requirements with

```bash
pip install -r requirements.txt
```

## Dash

The Dash app can be run with `python dash-app.py`

## Panel

The Panel app can be run with `panel serve panel-app.py`.

You can add the `--autoreload` flag while developing.

![Panel NYC Taxi App](assets/panel-nyc-taxi.gif)

## Streamlit

To run the streamlit app call `streamlit run streamlit-app.py`

## Shiny for Python

The python shiny app can be run with `shiny run shiny-app.py --reload`.

## Shiny for R

The R shiny app can be run with `R -e "shiny::runApp('app.R')"`.
