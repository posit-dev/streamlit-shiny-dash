import streamlit as st
from pandas import read_csv

from plots import plot_hist, plot_tips

if "count" not in st.session_state:
    st.session_state.count = 0


def increment_counter():
    st.session_state.count += 1


with st.sidebar:
    sample_ui = st.number_input(
        "sample", 0.0, 1.0, value=0.1, step=0.01, on_change=increment_counter
    )
    log = st.checkbox("Log Scale")


@st.cache_data
def load_data():
    df = read_csv("nyc-taxi.csv")
    return df


data = load_data()


@st.cache_data(max_entries=2)
def take_sample_busted(df, fraction, counter):
    return df.copy().sample(frac=fraction)


# We need to use this cache busting approach because otherwise the
# sample will be retrieved from cache instead of taking a new sample each
# time the sample size changed.
busted_sample = take_sample_busted(data, sample_ui, st.session_state.count)

st.subheader(f'Sample id: {busted_sample["taxi_id"].iloc[0]}')
st.pyplot(plot_tips(busted_sample, log))
st.pyplot(plot_hist(busted_sample))
