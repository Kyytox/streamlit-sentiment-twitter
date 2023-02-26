import os
import datetime
import calendar
import streamlit as st
import pandas as pd


# lib for graphs
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# functions 
from processGraph import get_nb_tweets_sent
from processGraph import get_data_interactions
from frequentsWords import get_frequent_words


sentiments = ['Positive','Neutral','Negative']

# color in graphs
# colors = ["rgb(0,114,27)", "rgb(195,195,0)", "rgb(145,0,13)"]
colors = ["rgb(145,0,13)", "rgb(195,195,0)", "rgb(0,114,27)"]


def display_graphs(df):   


    #  display the graph line of the score by day
    st.subheader('Moyenne des scores par sentiment')
    st.plotly_chart(_get_line_chart_score(df),use_container_width=True)


    # Graph 1 - 2
    col1, col2 = st.columns([7,10])
    with col1:
        # Pie charts 
        # distribution of the number of tweets by sentiments
        col1.plotly_chart(_get_pie_charts_by_sent(df),use_container_width=True)
    with col2:
        # Bar charts 
        # number of tweets by Sentiments 
        _get_bar_charts_by_sent(df)


    # # Graph 3 - 4
    # col3, col4 = st.columns([7,10])
    # with col3:
    #     # Bar Charts Month 
    #     # Number of tweets by month
    #     _get_bar_charts_day(df)
    # with col4:
    #     # Bar Charts Day
    #     # Number of tweets by day
    #     _get_bar_charts_month(df)


    # # 
    # # Interactions
    # with st.container():
    #     df_data_interac = get_data_interactions(df)
    #     col5, col6 = st.columns(2)
    #     with col5:
    #         _get_bar_charts_interactions(df_data_interac)

    #     with col6:
    #         _get_pie_charts_interactions(df_data_interac)


    # # 
    # # Frequents words
    # # with st.spinner("Loading word cloud ..."):
    # list_frequent_words = get_frequent_words(df)
    # text_wordCloud = ' '.join([f"{d['text']} " * d['value'] for d in list_frequent_words])
    # wordcloud = WordCloud(width=600, height=400, max_font_size=90, collocations=False, colormap="Reds").generate(text_wordCloud)

    # with st.container():
    #     _get_wordcloud(wordcloud)




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
    fig2 = px.bar(data_bar, x='sentiment', y='nb_tweets', color='sentiment', color_discrete_sequence=colors, labels={'nb_tweets':'Nombre tweets analysés'},text_auto='.2s')
    fig2.update_traces(textfont_size=16, textangle=0, textposition="outside", cliponaxis=False)
    st.subheader('Bar data')
    st.plotly_chart(fig2,use_container_width=True)



# Score line chart
# Mean of score by day and by sentiment
def _get_line_chart_score(df):

    lst_options = ['par jour', 'tout les 3 jours', 'par semaine', 'par mois']    
    freq_option = st.radio('Fréquence de temps :', lst_options, index=0, horizontal=True, key=1)

    # use match case to select the frequency of the graph
    match freq_option:
        case 'par jour':
            freq_option = 'D'
        case 'tout les 3 jours':
            freq_option = '3D'
        case 'par semaine':
            freq_option = 'W'
        case 'par mois':
            freq_option = 'M'

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

    report_year = st.selectbox('', range(this_year, this_year - 4, -1), index=1, key=1)
    # report_year = get_selected_year(this_year)

    data = df_data_bar_month[df_data_bar_month['date_tweet'].dt.strftime("%Y").str.startswith(f'{report_year}')]

    fig3 = px.bar(data, x='date_tweet', y='nb_tweets', color='sentiment', color_discrete_sequence=colors, labels={'nb_tweets':'Nombre tweets'},text_auto='.2s')
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
    report_month_str = st.radio('', month_name_lst, index=this_month - 2, horizontal=True, key=4)
    report_month = list(calendar.month_name).index(report_month_str)

    # filter dataframe by year and month
    df_data_bar_month = df_data_bar_month[df_data_bar_month['date_tweet'].dt.strftime("%Y-%m").str.startswith(f'{report_year}-{"{:02d}".format(report_month)}')]

    fig4 = px.bar(df_data_bar_month, x='date_tweet', y='nb_tweets', color='sentiment', color_discrete_sequence=colors, labels={'nb_tweets':'Nombre tweetswwwwww '},text_auto=True)
    fig4.update_traces(textfont_size=14, textangle=0, cliponaxis=False)
    st.plotly_chart(fig4,use_container_width=True)



def _get_bar_charts_interactions(df):
    fig5 = px.bar(df, x="sentiment", y="count", color="interactions", color_discrete_sequence=['rgb(0, 186, 24)', 'rgb(29, 155, 240)','rgb(249, 24, 128)', 'rgb(218, 223, 0)'] , text="interactions")
    fig5.update_traces(hovertemplate='%{label}<br>%{value}') # data when hover graph
    st.plotly_chart(fig5, use_container_width=True)


def _get_pie_charts_interactions(df):
    fig6 = px.sunburst(df, path=["sentiment","interactions"], values='count', color='sentiment', color_discrete_sequence=["rgb(145,0,13)","rgb(195,195,0)", "rgb(0,114,27)"])
    fig6.update_traces(hovertemplate='%{label}<br>%{value}') # data when hover graph 
    st.plotly_chart(fig6,use_container_width=True)


# Word Cloud
def _get_wordcloud(wordcloud):
    # Display the generated Word Cloud
    fig, ax = plt.subplots(figsize = (4, 4))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    ax.margins(x=0, y=0)
    st.subheader('Mots les plus fréquents')
    st.pyplot(fig)
