import streamlit as st
from langchain.prompts import PromptTemplate



# Page Content
st.title("About CampusBOLT")
st.write("") # Padding


st.write("**Millions of students use university directories to find vital information.**")
st.write("")

st.write("**These directories are plagued by issues such as:**")
st.write("&nbsp; 📚&nbsp;  Information overload.")
st.write("&nbsp; 🐌&nbsp; Finding what you need takes too long.")
st.write("&nbsp; 👎&nbsp; Poor navigation and search functionality.")
# Padding
st.write("")  
st.write("")


st.write("**CampusBOLT addresses these issues through:**")
st.write("&nbsp; 💬&nbsp; Intuitive chat interface.")
st.write("&nbsp; 🚀&nbsp; Instant and precise answers.")
st.write("&nbsp; 🔎&nbsp; Accurate info retrieval with source and resource links.")


# Padding
st.write("")  
st.write("")




st.subheader("Tech Stack")
st.write("")  

# Display tech stack icons
col1, col2, col3, col4, col5 = st.columns(5)


with col1:
    st.image("assets/mistral-ai-icon-seeklogo.svg", width=50)
    st.write("<div style='text-align: left; font-size: 14px;'>Mistral</div>", unsafe_allow_html=True)

with col2:
    st.image("assets/GroqLogo_White.png", width=45)
    st.write("<div style='text-align: left; font-size: 14px;'>groq</div>", unsafe_allow_html=True)

with col3:
    st.image("assets/neon-icon-seeklogo.svg", width=45)
    st.write("<div style='text-align: left; font-size: 14px;'>Neon</div>", unsafe_allow_html=True)

with col4:
    st.image("assets/langchain-seeklogo.svg", width=90)
    st.write("<div style='text-align: left; font-size: 14px;'>LangChain</div>", unsafe_allow_html=True)

with col5:
    st.image("assets/streamlit-seeklogo.svg", width=80)
    st.write("<div style='text-align: left; font-size: 14px;'>Streamlit</div>", unsafe_allow_html=True)

