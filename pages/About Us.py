import streamlit as st
from langchain.prompts import PromptTemplate



# Page Content
st.title("👋 About Us")
st.write("") # Padding


st.write("We are a team of experts leveraging cutting-edge technologies to build amazing applications.")
st.write("Our tech stack includes:")
st.write("- Mistral: A powerful tool for managing and deploying machine learning models.")
st.write("- Neon: A high-performance deep learning framework.")
st.write("- LangChain: A library for building applications with large language models.")
st.write("- Streamlit: A framework for creating interactive web applications.")


# Padding
st.write("")  
st.write("")



st.subheader("Tech Stack")
st.write("")  

# Display tech stack icons
col1, col2, col3, col4 = st.columns(4)


with col1:
    st.image("assets/mistral-ai-icon-seeklogo.svg", width=50)
    st.write("<div style='text-align: left; font-size: 14px;'>Mistral</div>", unsafe_allow_html=True)

with col2:
    st.image("assets/neon-icon-seeklogo.svg", width=45)
    st.write("<div style='text-align: left; font-size: 14px;'>Neon</div>", unsafe_allow_html=True)

with col3:
    st.image("assets/langchain-seeklogo.svg", width=90)
    st.write("<div style='text-align: left; font-size: 14px;'>LangChain</div>", unsafe_allow_html=True)

with col4:
    st.image("assets/streamlit-seeklogo.svg", width=80)
    st.write("<div style='text-align: left; font-size: 14px;'>Streamlit</div>", unsafe_allow_html=True)

