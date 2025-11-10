import streamlit as st
import pandas as pd
import numpy as np

st.title("Dashboard title")
st.header("section Header")
st.subheader("subsection")
st.write("Markdown, numbers, dataframes, floats, strs")
st.markdown("**Pau**_Pau_´code´ ")

name = st.text("Model Name")
options = st.selectbox ("Choose a model", ["CNN", "RNN", "YOLO", "Diffusion"])
threshold = st.slider("Confidence threshold",0.0,1.0,1.5)
run_button = st.button("run inference")

df = pd.DataFrame(np.random.randn(20,3),columns=["a","b","c"])
st.dataframe(df)
st.line_chart(df)