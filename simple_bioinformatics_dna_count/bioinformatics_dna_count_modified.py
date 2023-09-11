import pandas as pd
import streamlit as st
import altair as alt
from PIL import Image
import time

# Page title - 
image  = Image.open("dna-logo.jpg")

st.image(image, use_column_width=True)

st.write("""
# DNA Nucleotide Count Web App
         
This app counts the nucleotide composition of query DNA
         
""")
         
choice = st.text_input("Would you like to enter DNA query by urself or want to use a file for it?")
time.sleep(5)
if choice.lower() == 'yes':
    st.header("Enter DNA Sequence")
    sequence = st.text_area("Enter your query here", height=215)
    st.write("""
        ***
    """)
    st.header("Input (DNA Query)")
    sequence

    st.header("OUTPUT (DNA Nucleotide count)")

    st.subheader('1. Print Dictionary')

    def DNA_nucleotide_dict(seq):
        d = dict([
            ('A', seq.count('A')),
            ('T', seq.count('T')),
            ('G', seq.count('G')),
            ('C', seq.count('C'))

        ])

        return d
    X = DNA_nucleotide_dict(sequence)
    X
    st.subheader("Printing table")
    df = pd.DataFrame.from_dict(X, orient='index')
    df = df.rename({0: 'count'}, axis='columns')
    df = df.reset_index()
    df = df.rename({'index': 'nucleotide'}, axis='columns')
    st.write(df)

    st.subheader("Visualization using altair")
    p = alt.Chart(df).mark_bar().encode(
        x = 'nucleotide',
        y = 'count'
    )
    p = p.properties(
        width=alt.Step(80)
    )
    st.write(p)
# Input text box - 
else:

    st.header("We are taking DNA sequence data!")
    data = pd.read_table(choice)
    data.reset_index(inplace=True)
    del data["index"]
    del data['class']
    data = data['sequence']
    li = []
    for i in data:
        li.append(i)

    st.write("""
    *** 
    """) # This prints a line.

    st.header("input (DNA Query) sample")
    li[0]

    # DNA nucleotide count - 

    st.header("OUTPUT (DNA Nucleotide count)")

    # 1) Print Dictionary

    # st.subheader('1. Print Dictionary')

    def DNA_nucleotide_count(li):
        for j,i in enumerate(li[:10]):

            d = dict([
                ('A', i.count('A')),
                ('T', i.count('T')),
                ('G', i.count('G')),
                ('C', i.count("C"))
            ])
            j
            st.subheader("Printing DNA data")
            i
            st.subheader("Printing DNA Nucleotides count for above data")
            df = pd.DataFrame.from_dict(d, orient="index")
            df = df.rename({0: 'count'}, axis='columns')
            df.reset_index(inplace=True)
            df = df.rename(columns= {'index': 'nucleotide'})
            st.write(df)

            st.subheader("Displaying barchart using altair for above DNA data")
            p = alt.Chart(df).mark_bar().encode(
            x = 'nucleotide',
            y = 'count'
            )

            p = p.properties(
            width=alt.Step(80) # controls width of chart
            )
            st.write(p)

    DNA_nucleotide_count(li)
