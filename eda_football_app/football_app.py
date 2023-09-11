import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import base64

st.title("NFL Player Stats Explorer")
st.markdown("""
This app performs simple webscrapingof NFL players stats data

* **Python Libraries:** base64, numpy, python, matplotlib, seaborn, streamlit
* **Data Source:** [Pro-Football-Reference](https://www.pro-football-reference.com/)
""")
            
st.sidebar.header("User input features")
selected_year = st.sidebar.selectbox('Year', list(reversed(range(1990, 2020))))

# Web scraping and Data preprocessing starts - 
# https://www.pro-football-reference.com/years/2019/rushing.htm

@st.cache_data
def load_data(year):
    url = 'http://www.pro-football-reference.com/years/' + str(selected_year) + '/rushing.htm'
    htm = pd.read_html(url, header=0)
    df = htm[0]
    df.columns = df.iloc[0]
    df = df.drop(df[df.Age == 'Age'].index)
    df = df.fillna(0)
    df = df.drop(['Rk'], axis=1)
    return df
playerstats = load_data(selected_year)
# playerstats

# Sidebar - team selection
sorted_unique_teams = sorted(playerstats['Tm'].unique())
selected_team = st.sidebar.multiselect('Select team(s)', sorted_unique_teams, sorted_unique_teams)

# Sidebar - position selection - 

sorted_unique_pos = sorted(playerstats['Pos'].unique())
selected_pos = st.sidebar.multiselect('Selected position(s)', sorted_unique_pos, sorted_unique_pos)

# Filtering data - 
df_selected_team = playerstats[(playerstats.Tm.isin(sorted_unique_teams) & (playerstats.Pos.isin(sorted_unique_pos)))]

st.header('Display player stats based on selected team(s)')
st.write('Data Dimensions: ' + str(df_selected_team.shape[0]) + ' rows and ' + str(df_selected_team.shape[1]) + ' columns')
st.dataframe(df_selected_team)

# Download NFL Player stats data - 
def filedownload(df):
    csv = df.to_csv(index = False) # First index columns dropping
    b64 = base64.b64encode(csv.encode()).decode() #string -> byte
    href = f"<a href= 'data:file/csv;base64,{b64}' download='playerstats.csv'>Download CSV file</a>"
    return href

st.markdown(filedownload(df_selected_team), unsafe_allow_html=True)

# Heatmap - 
if st.button('Intercorrelation Heatmap'):
    st.header('Intercorrelation Matrix Heatmap')
    df_selected_team.to_csv('output.csv',index=False)
    df = pd.read_csv('output.csv')

    corr = df.corr(numeric_only=True) # Compute pairwise correlation of columns, 
                                      # excluding NA/null values
    mask = np.zeros_like(corr) # Return an array of zeros with the same shape and type 
                                # as a given array.
    mask[np.triu_indices_from(mask)] = True # Return the indices for the upper-triangle of arr.
    sns.axes_style("white") #Get the parameters that control the general style of the plots.
    f, ax = plt.subplots(figsize=(7, 5))
    ax = sns.heatmap(corr, mask=mask, vmax=1, square=True)
    st.set_option('deprecation.showPyplotGlobalUse', False) # To hide the global use issue.
    st.pyplot()
