import streamlit as st
from pandas import read_csv
from plotnine import ggplot, geom_point, geom_histogram, aes, theme_bw, scale_x_log10, scale_y_log10

if 'count' not in st.session_state:
	st.session_state.count = 0

def increment_counter():
	st.session_state.count += 1

with st.sidebar:
    sample_ui = st.number_input("sample", 0.0, 1.0, value = 0.1, step=0.01, on_change = increment_counter)
    log = st.checkbox("Log Scale")

@st.cache_data
def load_data():
    df = read_csv('nyc-taxi.csv')
    return df

data = load_data()

@st.cache_data
def take_sample_cached(df, fraction):
     return df.copy().sample(frac = fraction)

def take_sample_uncached(df, fraction):
     return df.copy().sample(frac = fraction)

def tip_plot(sample):
    plot = (ggplot(sample, aes('tip_amount', 'total_amount'))
           + geom_point()
           + theme_bw()
               )
    if log:
            plot = (plot
                    + scale_x_log10()
                    + scale_y_log10())
    return plot

def amount_histogram(df):
   plot = (
        ggplot(df, aes(x='total_amount'))
        + geom_histogram(binwidth = 5)
        + theme_bw()
    )
   return plot

sample_data_cached = take_sample_cached(data, sample_ui)
sample_data_uncached = take_sample_uncached(data, sample_ui)

st.header("Caching is incorrect")

st.markdown("""
The streamlit execution model causes everything to be re-executed whenever something
minor changes. Here a new random sample is taken whenever the plot options are changed. 
Note that the first taxi is and histogram change when you click 'log scale'. 

Caching the data solves this problem but creates incorrect behaviour because the 
data is returned from cache instead of taking a new sample. Notice that if you change the 
sample size from 0.1 to 0.11 and then back ot 0.1, the first taxi id swaps between two 
values instead of taxing a new random draw.
""")

col1, col2 = st.columns(2)

with col1:
    st.header('Uncached Tip plot')
    st.subheader(f'First taxi id: {sample_data_uncached["taxi_id"].iloc[0]}')

    tips = tip_plot(sample_data_uncached)
    st.pyplot(tips.draw())

    amounts = amount_histogram(sample_data_uncached)
    st.pyplot(amounts.draw())

with col2:
    st.header('Cached tip plot')
    st.subheader(f'First taxi id: {sample_data_cached["taxi_id"].iloc[0]}')
                
    tips_cached = tip_plot(sample_data_cached)
    st.pyplot(tips_cached.draw())

    amounts_cached = amount_histogram(sample_data_cached)
    st.pyplot(amounts_cached.draw())    


st.header("Callbacks and cache busting can help")

st.markdown("""
We can add a callback function to the sample selector which increrments a cache-busting counter.
When the this counter is passed to the sampling function it will invalidate the cache and 
take a new sample. 

This creates its own problems though because every sampled dataset will be held in memory which 
can lead to app crashes. In order to fix _that_ problem we can add a `max_entries` argument to only
hold two entries in cache. However if we then add additional plot options, `max_entries` will need 
to be updated to be bigger than the product of the available options.
""")

@st.cache_data(max_entries = 2)
def take_sample_busted(df, fraction, counter):
    return df.copy().sample(frac= fraction)


busted_sample = take_sample_busted(data, sample_ui, st.session_state.count)

st.subheader(f'First taxi id: {busted_sample["taxi_id"].iloc[0]}')
st.markdown(f'Increment counter {st.session_state.count}')
tips_busted = tip_plot(busted_sample)
st.pyplot(tips_busted.draw())