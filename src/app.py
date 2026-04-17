# import streamlit as st
# import pandas as pd
# import networkx as nx
# import matplotlib.pyplot as plt
# from pathlib import Path

# BASE_DIR = Path(__file__).resolve().parent.parent
# DATA_PATH = BASE_DIR / "data" / "processed_data" / "skincare_data.csv"

# df = pd.read_csv(DATA_PATH)
# G = nx.DiGraph()

# for _, row in df.iterrows():
#     G.add_edge(row['Product'], row['Most Similar'], weight=row['Similarity Score'])

# in_degree = dict(G.in_degree())
# df['in_degree'] = df['Product'].map(in_degree).fillna(0).astype(int)

# st.title("Skincare Product Similarity Explorer")

# product = st.selectbox("Select a product", df['Product'].unique())

# st.subheader("Anchor Score")
# st.write(df[df['Product'] == product]['in_degree'].values[0])

# st.subheader("Products that consider this similar")
# incoming = list(G.predecessors(product))
# st.write(incoming)

# subG = G.subgraph(incoming + [product])

# pos = nx.spring_layout(subG, k=1.2, seed=42)
# nx.draw(subG, pos, with_labels=True, node_size=1500, arrows=True)
# st.pyplot(plt)


import streamlit as st
import pandas as pd
import networkx as nx
from pathlib import Path
import matplotlib.pyplot as plt

# ----------------------------
# LOAD DATA
# ----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "processed_data" / "skincare_data.csv"

df = pd.read_csv(DATA_PATH)

# ----------------------------
# BUILD GRAPH
# ----------------------------
G = nx.DiGraph()

for _, row in df.iterrows():
    G.add_edge(row["Product"], row["Most Similar"], weight=row["Similarity Score"])

# in-degree (anchor score)
in_degree = dict(G.in_degree())
df["in_degree"] = df["Product"].map(in_degree).fillna(0).astype(int)

# ensure cluster exists (from Louvain step)
# df["cluster"] should already exist from preprocessing

# ----------------------------
# SIDEBAR CONTROLS
# ----------------------------
st.sidebar.title("🔍 Controls")

# ----------------------------
# CLUSTER FILTER (optional exploration)
# ----------------------------
cluster_options = sorted(df["cluster"].unique())
selected_cluster = st.sidebar.selectbox(
    "Browse by Cluster (optional)",
    ["All"] + cluster_options
)

if selected_cluster == "All":
    cluster_df = df
else:
    cluster_df = df[df["cluster"] == selected_cluster]

# ----------------------------
# GLOBAL PRODUCT SEARCH (ALWAYS AVAILABLE)
# ----------------------------
product = st.sidebar.selectbox(
    "🔎 Search Product (Global)",
    sorted(df["Product"].unique())
)

# ----------------------------
# MAIN PANEL
# ----------------------------
st.title("Skincare Similarity Explorer")

row = df[df["Product"] == product].iloc[0]

# --- PRODUCT INFO ---
st.subheader("📌 Product Overview")
st.write(product)

st.metric("⭐ Anchor Score (In-Degree)", int(row["in_degree"]))

# --- WARNINGS ---
st.subheader("⚠️ Compatibility Warnings")

if "Caution" in df.columns:
    warnings = row["Caution"]

    if pd.isna(warnings) or warnings == "":
        st.success("No known conflicts detected.")
    else:
        if isinstance(warnings, list):
            for w in warnings:
                st.warning(w)
        else:
            st.warning(warnings)
else:
    st.info("No warning data available.")

# --- INCOMING SIMILAR PRODUCTS ---
st.subheader("🔁 Products that consider this similar")

incoming = list(G.predecessors(product))

if incoming:
    st.write(incoming)
else:
    st.write("No incoming similarity links.")

# ----------------------------
# OPTIONAL: GRAPH VIEW (EGO NETWORK)
# ----------------------------
st.subheader("🕸 Local Similarity Network")

sub_nodes = incoming + [product]
subG = G.subgraph(sub_nodes)

pos = nx.spring_layout(subG, k=1.2, seed=42)

fig, ax = plt.subplots(figsize=(6, 5))
nx.draw(
    subG,
    pos,
    with_labels=True,
    node_size=1200,
    arrows=True,
    ax=ax
)

st.pyplot(fig)