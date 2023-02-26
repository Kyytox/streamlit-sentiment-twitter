import time
import streamlit as st
import numpy as np


import plotly.graph_objects as go
from displayGraphs import _get_pie_charts_by_sent


sentiments = ['Positive','Neutral','Negative']

# color in graphs
# colors = ["rgb(0,114,27)", "rgb(195,195,0)", "rgb(145,0,13)"]
colors = ["rgb(145,0,13)", "rgb(195,195,0)", "rgb(0,114,27)"]

# Pie charts 
# distribution of the number of tweets by sentiments
def page_accueil(df):

    with st.container():
        # display bar charts of number of tweets by user
        fig = _get_bar_chart_nb_tweets_by_user(df)
        st.plotly_chart(fig, use_container_width=True)
    # create container
    with st.container():
        #  call the function to display the pie charts
        display_pie_charts(df)







# Pie charts
# for each user in the dataframe create a pie chart 
# the pie chart is the distribution of the number of tweets by sentiments
def display_pie_charts(df):
    # Create a list to store all the figure placeholders
    list_fig = []

    list_user = df['name_user'].unique()

    for user in list_user:

        # get data for the user
        df_user = df.loc[df['name_user'] == user]

        # replace the placeholder with the figure
        fig = _get_pie_charts_by_sent(df_user)
        
        print(df_user.columns)

        # count line in the dataframe and upadet layout with new subtitle
        nb_tweets = df_user.shape[0]
        fig.update_layout(
            title=dict(
                text=f"{user}",
            ),
            showlegend=False,
            annotations=[dict(text=f"{nb_tweets} tweets analysés", x=0.01, y=1.17, font_size=15, showarrow=False)]
        )
        
        # update the hover text
        fig.update_traces(hoverinfo='label+value', textfont_size=15)

        # add the figure to the list
        list_fig.append(fig)


    n_charts = len(list_fig)

    # display pie charts 3 by 3
    n_cols = 5
    for i in range(0, n_charts, n_cols):
        # create columns for each pie chart
        columns = st.columns(min(n_charts-i, n_cols))

        # display each pie chart in a separate column
        for j, col in enumerate(columns):
            fig_index = i + j
            if fig_index < n_charts:
                col.plotly_chart(list_fig[fig_index], use_container_width=True)





# bar charts of number of tweets by user
def _get_bar_chart_nb_tweets_by_user(df):
    # get the number of tweets by user
    df_nb_tweets = df.groupby('name_user').size().reset_index(name='nb_tweets')

    # sort the dataframe by number of tweets
    df_nb_tweets = df_nb_tweets.sort_values(by=['nb_tweets'], ascending=False)

    # create the bar chart
    fig = go.Figure(data=[go.Bar(
        x=df_nb_tweets['name_user'],
        y=df_nb_tweets['nb_tweets'],
        marker_color=colors[0],
        opacity=0.8
    )])

    # update the layout
    fig.update_layout(
        title=dict(
            text="Nombre de tweets par utilisateur",
        ),
        xaxis_title="Compte Twitter",
        yaxis_title="Nombre de tweets",
        showlegend=False,
        margin=dict(l=0, r=0, t=40, b=0),
        height=400
    )

    return fig
