import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import base64
import seaborn as sns
import numpy as np

# st.write("""
# # NBA Player Satas Explorer""")
st.title("NBA Player Stats Explorer") # This is same as above.
st.markdown("""
This app performs simple webscraping of NBA players stats data!

* **Python Libraries:** base64, pandas, streamlit
* **Data Source:** [Basketball-reference.com](https://www.basketball-reference.com/).
""")
            
st.sidebar.header("User input features")
selected_year = st.sidebar.selectbox('Year', list(reversed(range(1950, 2020))))


# Web scraping and data preprocessing begins - 
# @st.cache - When you mark a function with Streamlit’s cache annotation, it tells Streamlit that whenever the function is called it should check three things:
    # The name of the function
    # The actual code that makes up the body of the function
    # The input parameters that you called the function with
#   Decorator to cache functions that return data (e.g. dataframe transforms, 
#   queries, ML inference).

# Cached objects are stored in "pickled" form, which means that the return value of a 
# cached function must be pickleable. Each caller of the cached function gets its own 
# copy of the cached data.

# What is pickle format? 
#   Python's Pickle module is a popular format used to serialize and deserialize data 
#   types. This format is native to Python, meaning Pickle objects cannot be loaded using 
#   any other programming language.
# The name "pickle" comes from the concept of "pickling" in cooking, which refers to 
# the process of preserving food by storing it in a container. In the same way, the 
# Python pickle module preserves and stores objects by converting them into a byte stream

@st.cache_data
def load_data(year):
    url = 'http://www.basketball-reference.com/leagues/NBA_' + str(year) + '_per_game.html'
    html = pd.read_html(url, header=0) # This contains list of tables.
    df = html[0] # selecting first table from html tables list.
    raw = df.drop(df[df['Age'] == 'Age'].index) # Deletes repeating headers in content/ Rows
    # where there is no data are deleted.
    raw = raw.fillna(0) # We could have used SimpleInputer to fill null values.
    playerstats = raw.drop(['Rk'], axis=1)
    return playerstats
playerstats = load_data(selected_year)    

#Sidebar - Team Selection 
sorted_unique_team = sorted(playerstats.Tm.unique())
selected_team = st.sidebar.multiselect('Team', sorted_unique_team, sorted_unique_team)

# Sidebar - Position Selection
unique_pos = ['C', 'PF', 'SF', 'PG', 'SG']
selected_pos = st.sidebar.multiselect('Position', unique_pos, unique_pos)

#Filtering data - 
df_selected_team = playerstats[(playerstats.Tm.isin(selected_team) & (playerstats.Pos.isin(selected_pos)))]

st.header("Display player stats of seleted team(s)")
st.write("Data Dimensions: " + str(df_selected_team.shape[0]) + " rows and " + str(df_selected_team.shape[1]) + " columns.")
st.dataframe(df_selected_team)

# Download NBA player stats data
# https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806

def filedownload(df):
    csv = df.to_csv(index = 'False') # first index columns dropping
    b64 = base64.b64encode(csv.encode()).decode() # string -> bytes conversion
    href = f"<a href='data:file/csv;base64,{b64}' download='playerstats.csv'>Download CSV file </a>"
    return href

st.markdown(filedownload(df_selected_team), unsafe_allow_html=True)

# Heatmap
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