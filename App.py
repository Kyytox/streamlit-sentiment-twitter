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


import pandas as pd

from displayGraphs import display_graphs
from Accueil import page_accueil


# retriev csv file of folder ./data_csv
st.cache()
def get_csv_file():
    file_name = "./data_csv/data-tweets.csv"
    df = pd.read_csv(file_name)
    df['date_tweet'] = pd.to_datetime(df['date_tweet'], errors='coerce')
    lst_name_user = list(df['name_user'].unique())
    # lst_name_user.insert(0, "Accueil")
    return [lst_name_user, df]



st.cache()
def main():
    # define width of page web 
    st.set_page_config(layout="wide")
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

        # CSS for the sidebar
        [data-testid="stSidebar"][aria-expanded="true"] {
            width: 100px;
        }
        </style>
        
        """,
        unsafe_allow_html=True,
    )

    lst_name_user, df = get_csv_file()
    selected_user = st.sidebar.selectbox("Choississez un des compte twitter qui a été analysé", lst_name_user, key='user_selector')

    print("selected_user", selected_user)

    if selected_user != "Accueil":
        df = df[df['name_user'] == selected_user]
        #Title
        st.title(f"Sentiment Twitter {selected_user}")
        display_graphs(df)
    else:
        st.title("Analyse des sentiments sur Twitter")
        page_accueil(df)




if __name__ == '__main__':
    main()