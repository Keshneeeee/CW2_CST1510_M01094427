import streamlit as st
from google import genai

st.title("Gemini Chat")

client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

prompt = st.text_input("Ask something")

if prompt:
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )

    st.write(response.text)






