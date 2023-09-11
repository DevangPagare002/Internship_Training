import pandas as pd
import streamlit as st
import altair as alt # Visualization library
from PIL import Image # Python imaging library

# Page title - 
image  = Image.open("dna-logo.jpg")

st.image(image, use_column_width=True)

st.write("""
# DNA Nucleotide Count Web App
         
This app counts the nucleotide composition of query DNA
         
""")
         
# Input text box - 

st.header("Enter DNA sequence")

sequence_input = ">DNA Query 2\nGAACACGTGGAGGCAAACAGGAAGGTGAAGAAGAACTTATCCTATCAGGACGGAAGGTCCTGTGCTCGGG\nATCTTCCAGACGTCGCGACTCTAAATTGCCCCCTCTGAGGTCAAGGAACACAAGATGGTTTTGGAAATGC\nTGAACCCGATACATTATAACATCACCAGCATCGTGCCTGAAGCCATGCCTGCTGCCACCATGCCAGTCCT"
sequence = st.text_area("Sequence input given", sequence_input, height=215)
sequence = sequence.splitlines()
sequence = sequence[1:] #skips the sequence name i.e. first line.
sequence = "".join(sequence)

st.write("""
*** 
""") # This prints a line.

st.header("input (DNA Query)")
sequence

# DNA nucleotide count - 

st.header("OUTPUT (DNA Nucleotide count)")

# 1) Print Dictionary

st.subheader('1. Print Dictionary')

def DNA_nucleotide_count(seq):
    d = dict([
        ('A', seq.count('A')),
        ('T', seq.count('T')),
        ('G', seq.count('G')),
        ('C', seq.count("C"))
    ])
    return d

X = DNA_nucleotide_count(sequence)

X
# 2) Print the text - 

st.subheader("2. Print text")
df = pd.DataFrame.from_dict(X, orient="index") # orientation - if we want keys to be rows, select index, else column
df = df.rename({0: 'count'}, axis='columns')
df.reset_index(inplace=True)
df = df.rename(columns= {'index': 'nucleotide'})
st.write(df)

# 3) Display barchart using altair - 

st.subheader("3. Display barchart using altair")
p = alt.Chart(df).mark_bar().encode(
    x = 'nucleotide',
    y = 'count'
)

p = p.properties(
    width=alt.Step(80) # controls width of chart
)
st.write(p)