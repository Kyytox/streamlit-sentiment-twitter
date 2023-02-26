import datetime
import calendar
import streamlit as st
import pandas as pd


# lib for graphs
import plotly.express as px
import plotly.graph_objects as go

# functions 
from processGraph import get_nb_tweets_sent
from widgets import _get_freq_option


sentiments = ['Positive','Neutral','Negative']

# color in graphs
# colors = ["rgb(0,114,27)", "rgb(195,195,0)", "rgb(145,0,13)"]
colors = ["rgb(145,0,13)", "rgb(195,195,0)", "rgb(0,114,27)"]


##################################################
# Graphs Sentiments 

# Pie charts 
# distribution of the number of tweets by sentiments
def _get_pie_charts_by_sent(df):
    data_pie = get_nb_tweets_sent(df)
    return go.Figure(
        data=[
            go.Pie(
                labels=data_pie['sentiment'],
                values=data_pie['nb_tweets'],
                pull=[0.015, 0.015, 0.015],
                marker_colors=colors,
            )
        ]
    )


# Bar charts 
# number of tweets by Sentiments 
def _get_bar_charts_by_sent(df):
    data_bar = get_nb_tweets_sent(df)
    fig2 = px.bar(data_bar, x='sentiment', y='nb_tweets', color='sentiment', color_discrete_sequence=colors, labels={'nb_tweets':'Nombre tweets analysés'}, text='nb_tweets')
    fig2.update_traces(textfont_size=16, textangle=0, textposition="outside", cliponaxis=False)
    st.subheader('Bar data')
    st.plotly_chart(fig2,use_container_width=True)




# Score line chart
# Mean of score by freq_option and by sentiment
def _get_line_chart_score(df):

    freq_option = _get_freq_option(1)

    # group dataframe by day and sentiment and calculate the mean of score 
    # create a new data frame with 3 columns [date_tweet sentiment score]
    df_data_line = df.groupby([pd.Grouper(key='date_tweet',freq=freq_option), 'sentiment']).agg({'score': 'mean'}).reset_index()

    fig = px.line(df_data_line, 
                x='date_tweet', 
                y='score', 
                color='sentiment', 
                color_discrete_sequence=colors, 
                labels={'score':'Score moyen'},
                width=800,
                height=600)
    fig.update_traces(mode='lines+markers')
    return fig



# Bar Charts Day
# Number of tweets by day
def _get_bar_charts_day(df):
    # group dataframe by month and sentiment and count the nb of tweets  
    # create a new data frame with 3 columns [date_tweet sentiment count]
    df_data_bar_month = df.groupby([pd.Grouper(key='date_tweet',freq='M'), 'sentiment']).agg({'sentiment': 'size'}).rename(columns={'sentiment':'nb_tweets'}).reset_index()
    st.subheader('Bar Month data')

    # create slide menu with year 
    # create calendar with month  
    this_year = datetime.date.today().year

    report_year = st.selectbox('', range(this_year, this_year - 4, -1), index=1, key=5)
    # report_year = get_selected_year(this_year)

    data = df_data_bar_month[df_data_bar_month['date_tweet'].dt.strftime("%Y").str.startswith(f'{report_year}')]

    fig3 = px.bar(data, x='date_tweet', y='nb_tweets', color='sentiment', color_discrete_sequence=colors, labels={'nb_tweets':'Nombre tweets'},text='nb_tweets')
    # type: ignore    fig3.update_traces(textfont_size=16, textangle=0, textposition="outside", cliponaxis=False)
    st.plotly_chart(fig3,use_container_width=True)



# Bar Charts Month 
# Number of tweets by month
def _get_bar_charts_month(df):
    # group dataframe by day and sentiment and count the nb of tweets  
    # create a new data frame with 3 columns [date_tweet sentiment count]
    df_data_bar_month = df.groupby([pd.Grouper(key='date_tweet',freq='D'), 'sentiment']).agg({'sentiment': 'size'}).rename(columns={'sentiment':'nb_tweets'}).reset_index()
    st.subheader('Bar Day data')

    # create slide menu with year 
    # create calendar with month  
    this_year = datetime.date.today().year
    this_month = datetime.date.today().month
    report_year = st.selectbox('', range(this_year, this_year - 4, -1), key=3)
    month_name_lst = calendar.month_name[1:]
    report_month_str = st.radio('', month_name_lst, index=this_month - 1, horizontal=True, key=4)
    report_month = list(calendar.month_name).index(str(report_month_str))


    # filter dataframe by year and month
    df_data_bar_month = df_data_bar_month[df_data_bar_month['date_tweet'].dt.strftime("%Y-%m").str.startswith(f'{report_year}-{"{:02d}".format(report_month)}')]

    fig4 = px.bar(df_data_bar_month, x='date_tweet', y='nb_tweets', color='sentiment', color_discrete_sequence=colors, labels={'nb_tweets':'Nombre tweetswwwwww '},text_auto=True)
    fig4.update_traces(textfont_size=14, textangle=0, cliponaxis=False)
    st.plotly_chart(fig4,use_container_width=True)