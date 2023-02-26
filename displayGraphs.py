import streamlit as st

# lib for graphs
from wordcloud import WordCloud

# functions 
from processGraph import get_data_interactions

from frequentsWords import get_frequent_words

from graphsSentiments import _get_bar_charts_month
from graphsSentiments import _get_line_chart_score
from graphsSentiments import _get_pie_charts_by_sent
from graphsSentiments import _get_bar_charts_by_sent
from graphsSentiments import _get_bar_charts_day

from graphsInteractions import _get_line_chart_interactions
from graphsInteractions import _get_bar_charts_interactions
from graphsInteractions import _get_pie_charts_interactions

from graphsFrequentWords import _get_wordcloud



def display_graphs(df):   

    tab1, tab2, tab3 = st.tabs(["Sentiments", "Interactions", "Frequent Words"])

    # #
    # # Sentiments
    with tab1:
        tabs_sentiments(df)
            
    # #
    # # Interactions
    with tab2:
        tabs_interactions(df)
    
    # # 
    # # Frequents words
    with tab3:
        tabs_frequent_words(df)



##################################################
# Tabs Sentiments 

def tabs_sentiments(df):
    #  display the graph line of the score
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




##################################################
# Graphs interactions 

def tabs_interactions(df):
    #  display the graph line of the sum of interactions
    st.subheader('Somme des interactions')
    st.plotly_chart(_get_line_chart_interactions(df),use_container_width=True)


    with st.container():
        df_data_interac = get_data_interactions(df)
        col5, col6 = st.columns(2)
        with col5:
            _get_bar_charts_interactions(df_data_interac)

        with col6:
            _get_pie_charts_interactions(df_data_interac)



##################################################
# Graphs frequent words

def tabs_frequent_words(df):
    # with st.spinner("Loading word cloud ..."):
    list_frequent_words = get_frequent_words(df)
    text_wordCloud = ' '.join([f"{d['text']} " * d['value'] for d in list_frequent_words])
    wordcloud = WordCloud(width=600, height=400, max_font_size=90, collocations=False, colormap="Reds").generate(text_wordCloud)

    with st.container():
        _get_wordcloud(wordcloud)

