from google import genai
import streamlit as st

API_KEY = st.secrets.get("GEMINI_API_KEY")
model ="gemini-2.5-flash"
prompt = "Create a haiku based on software and electronic music"

client = genai.Client(api_key=API_KEY)

response = client.models.generate_content(model=model,contents=prompt)
print(response.text)
