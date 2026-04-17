import streamlit as st
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# assume df already exists
df = pd.read_csv("../data/skincare_data.csv")
G = nx.DiGraph()

for _, row in df.iterrows():
    G.add_edge(row['Product'], row['Most Similar'], weight=row['Similarity Score'])

in_degree = dict(G.in_degree())
df['in_degree'] = df['Product'].map(in_degree).fillna(0).astype(int)

st.title("Skincare Product Similarity Explorer")

product = st.selectbox("Select a product", df['Product'].unique())

st.subheader("Anchor Score")
st.write(df[df['Product'] == product]['in_degree'].values[0])

st.subheader("Products that consider this similar")
incoming = list(G.predecessors(product))
st.write(incoming)

# simple graph view (ego network)
subG = G.subgraph(incoming + [product])

pos = nx.spring_layout(subG, k=1.2, seed=42)
nx.draw(subG, pos, with_labels=True, node_size=1500, arrows=True)
st.pyplot(plt)