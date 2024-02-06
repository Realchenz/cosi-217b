from collections import Counter
from operator import itemgetter
from spacy import displacy

import streamlit as st
import pandas as pd
import altair as alt


import ner


example = (
        "When Sebastian Thrun started working on self-driving cars at "
        "Google in 2007, few people outside of the company took him "
        "seriously. “I can tell you very senior CEOs of major American "
        "car companies would shake my hand and turn away because I wasn’t "
        "worth talking to,” said Thrun, in an interview with Recode earlier "
        "this week.")

entities_container = st.container()
dependencies_container = st.container()


genre = st.sidebar.radio('Select View', ('entities', 'dependencies'), index=0, key=None)

if genre == 'entities':
    entities_container.write('## spaCy Named Entity Recognition')

    text = st.text_area('Text to process', value=example, height=100)

    doc = ner.SpacyDocument(text)

    entities = doc.get_entities()
    tokens = doc.get_tokens()
    counter = Counter(tokens)
    words = list(sorted(counter.most_common(30)))

    # https://pandas.pydata.org
    chart = pd.DataFrame({
        'frequency': [w[1] for w in words],
        'word': [w[0] for w in words]})

    # https://pypi.org/project/altair/
    bar_chart = alt.Chart(chart).mark_bar().encode(x='word', y='frequency')

    st.markdown(f'Total number of tokens: {len(tokens)}<br/>'
                f'Total number of types: {len(counter)}', unsafe_allow_html=True)

    # https://docs.streamlit.io/library/api-reference/data/st.table
    st.table(entities)

    # https://docs.streamlit.io/library/api-reference/charts/st.altair_chart
    st.altair_chart(bar_chart)

    dependencies_container.empty()
else:
    entities_container.empty()

    dependencies_container.write('## spaCy Dependency Parse')

    text = st.text_area('Text to process', value=example, height=100) 

    def display_table():
        doc = ner.SpacyDocument(text)
        
        # Get the dependency relationships for each sentence
        dependencies_table = []
        for token in doc.doc:
            dependencies_table.append({
                "Token": token.text,
                "Dependency": token.dep_,
                "Head Token": token.head.text,
                "Head POS": token.head.pos_,
            })
        
        st.table(dependencies_table)

    def display_dependency_tree():
        doc = ner.SpacyDocument(text)  
        # https://spacy.io/usage/visualizers
        st.subheader("Dependency Parse Tree")
        displacy_rendered = displacy.render(doc.doc, style="dep", options={'distance': 200})
        st.image(displacy_rendered)
    

    tab1, tab2 = st.tabs(['table', 'graph'])   

    with tab1:
        display_table()
    with tab2:
        display_dependency_tree()

