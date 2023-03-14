import streamlit as st

# element selector radio for the frequency of the graph
def _get_freq_option(index):
    lst_options = ['par jour', 'tout les 3 jours', 'par semaine', 'par mois']    
    freq_option = st.radio('Fréquence de temps :', lst_options, index=0, horizontal=True, key=index)

    print("freq_option", freq_option)

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

    return freq_option
