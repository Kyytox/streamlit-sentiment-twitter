import streamlit as st

# st.set_page_config(
#     page_title="Hello",
#     page_icon="👋",
# )

# st.write("# Welcome to Streamlit! 👋")

# st.sidebar.success("Select a demo above.")

# st.markdown(
#     """
#     Streamlit is an open-source app framework built specifically for
#     Machine Learning and Data Science projects.
#     **👈 Select a demo from the sidebar** to see some examples
#     of what Streamlit can do!
#     ### Want to learn more?
#     - Check out [streamlit.io](https://streamlit.io)
#     - Jump into our [documentation](https://docs.streamlit.io)
#     - Ask a question in our [community
#         forums](https://discuss.streamlit.io)
#     ### See more complex demos
#     - Use a neural net to [analyze the Udacity Self-driving Car Image
#         Dataset](https://github.com/streamlit/demo-self-driving)
#     - Explore a [New York City rideshare dataset](https://github.com/streamlit/demo-uber-nyc-pickups)
# """
# )

import os
import pandas as pd
import datetime
import calendar

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
colors = ["rgb(0,114,27)", "rgb(195,195,0)", "rgb(145,0,13)"]


def load_data(page):
    print("loadData")
    # convert page name to csv file name
    # ex: Bfm Tv => data_bfm_tv.csv
    print(page)
    page = page.lower().replace(' ','_')

    print(page)
    file_name = f"./data_csv/data_{page}.csv"
    # file_name = f"./data_csv/{page}"
    df = pd.read_csv(file_name)
    df['date_tweet'] = pd.to_datetime(df['date_tweet'], errors='coerce')
    return df


def extract_name_user(list_csv):
    # browse list of csv file and extract name of user 
    # ex: data_afp_fr.csv => Afp Fr
    list_user = []
    for csv in list_csv:
        user = csv.replace('data_','').replace('.csv','').replace('_',' ').title()
        list_user.append(user)
    
    print(list_user)
    return list_user




# retriev csv file of folder ./data_csv
def get_csv_file():
    path = "./data_csv"
    return extract_name_user(os.listdir(path))



def main():
    # define width of page web 
    # st.set_page_config(layout="wide")
    # CSS
    st.markdown(
        """
        <style>
        img {
            width: 620px !important;
            height: 413px !important;
            clip-path: rect(5px, 95px, 10%, 5px);
            object-fit: none;
            object-position: -20px -20px;
        }

        .css-1p1nwyz {
            width: 304px;
            position: relative;
            text-align: center;
        }
        .css-z09lfk {
            width: 77%;
        }
        </style>
        
        """,
        unsafe_allow_html=True,
    )

    pages = get_csv_file()

    # browse pages and display button for each page 
    # when click on button, display data of page
    page = "App"
    for user in pages:
        if st.sidebar.button(user):
            page = user

    if page != "App":
        df = load_data(page)
        display_graphs(df)
    else:
        st.title("Page d'accueil")






def display_graphs(df):   
    #Title
    st.title(f"Sentiment Twitter{page}")

    # Graph 1 - 2
    col1, col2 = st.columns([7,10])
    with col1:
        # Pie charts 
        # distribution of the number of tweets by sentiments
        _get_pie_charts_by_sent(df)
    with col2:
        # Bar charts 
        # number of tweets by Sentiments 
        _get_bar_charts_by_sent(df)


    # Graph 3 - 4
    col3, col4 = st.columns([7,10])
    with col3:
        # Bar Charts Month 
        # Number of tweets by month
        _get_bar_charts_day(df)
    with col4:
        # Bar Charts Day
        # Number of tweets by day
        _get_bar_charts_month(df)


    # 
    # Interactions
    with st.container():
        df_data_interac = get_data_interactions(df)
        col5, col6 = st.columns(2)
        with col5:
            _get_bar_charts_interactions(df_data_interac)

        with col6:
            _get_pie_charts_interactions(df_data_interac)



    # 
    # Frequents words
    with st.spinner("Loading word cloud ..."):
        list_frequent_words = get_frequent_words(df)
        text_wordCloud = ' '.join([f"{d['text']} " * d['value'] for d in list_frequent_words])
        wordcloud = WordCloud(width=600, height=400, max_font_size=90, collocations=False, colormap="Reds").generate(text_wordCloud)

        with st.container():
            _get_wordcloud(wordcloud)




# Pie charts 
# distribution of the number of tweets by sentiments
def _get_pie_charts_by_sent(df):
    data_pie = get_nb_tweets_sent(df)
    fig = go.Figure(data=[go.Pie(labels=data_pie['sentiment'], values=data_pie['nb_tweets'], pull=[0.015, 0.015, 0.015], marker_colors=colors)])
    st.subheader('Pie data')
    st.plotly_chart(fig,use_container_width=True)


# Bar charts 
# number of tweets by Sentiments 
def _get_bar_charts_by_sent(df):
    data_bar = get_nb_tweets_sent(df)
    fig2 = px.bar(data_bar, x='sentiment', y='nb_tweets', color='sentiment', color_discrete_sequence=colors, labels={'nb_tweets':'Nombre tweets analysés'},text_auto='.2s')
    fig2.update_traces(textfont_size=16, textangle=0, textposition="outside", cliponaxis=False)
    st.subheader('Bar data')
    st.plotly_chart(fig2,use_container_width=True)




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

    # report_year = st.selectbox('', range(this_year, this_year - 2, -2)+ ['2023'],default='2022', key=1)
    report_year = st.selectbox('', range(this_year, this_year - 4, -1), index=1, key=1)

    data = df_data_bar_month[df_data_bar_month['date_tweet'].dt.strftime("%Y").str.startswith(f'{report_year}')]

    fig3 = px.bar(data, x='date_tweet', y='nb_tweets', color='sentiment', color_discrete_sequence=colors, labels={'nb_tweets':'Nombre tweets'},text_auto='.2s')
    fig3.update_traces(textfont_size=16, textangle=0, textposition="outside", cliponaxis=False)
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

    df_data_bar_month = df_data_bar_month[df_data_bar_month['date_tweet'].dt.strftime("%Y-%m").str.startswith(f'{report_year}-{"{:02d}".format(report_month)}')]

    fig4 = px.bar(df_data_bar_month, x='date_tweet', y='nb_tweets', color='sentiment', color_discrete_sequence=colors, labels={'nb_tweets':'Nombre tweetswwwwww '},text_auto=True)
    fig4.update_traces(textfont_size=14, textangle=0, cliponaxis=False)
    st.plotly_chart(fig4,use_container_width=True)



def _get_bar_charts_interactions(df):
    fig5 = px.bar(df, x="sentiment", y="count", color="interactions", color_discrete_sequence=['rgb(0, 186, 24)', 'rgb(29, 155, 240)','rgb(249, 24, 128)', 'rgb(218, 223, 0)'] , text="interactions")
    fig5.update_traces(hovertemplate='%{label}<br>%{value}') # data when hover graph
    st.plotly_chart(fig5, use_container_width=True)


def _get_pie_charts_interactions(df):
    fig6 = px.sunburst(df, path=["sentiment","interactions"], values='count', color='sentiment', color_discrete_sequence=["rgb(0,114,27)", "rgb(145,0,13)", "rgb(195,195,0)"])
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


main()