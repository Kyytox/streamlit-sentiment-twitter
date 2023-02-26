import streamlit as st

import plotly.graph_objects as go
from displayGraphs import _get_pie_charts_by_sent
from processGraph import get_nb_tweets_sent


# Pie charts 
# distribution of the number of tweets by sentiments
def page_accueil(df):
    # for each user in the dataframe create a pie chart 
    # the pie chart is the distribution of the number of tweets by sentiments
    for user in df['name_user'].unique():
        
        # title
        st.title(f"Sentiment Twitter {user}")
        
        # get data for the user
        df_user = df.loc[df['name_user'] == user]
        # get data for the pie chart
        _get_pie_charts_by_sent(df_user)
        