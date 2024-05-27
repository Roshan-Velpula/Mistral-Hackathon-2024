﻿# Mistral-Hackathon-2024

# CampusBOLT

![Project Banner](https://via.placeholder.com/800x200.png?text=Student+Advisor+Chatbot)


## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Contributors](#contributors)

## Introduction
The **CampusBOLT** is a robust solution designed to assist students with administrative queries using RAG and LLMs. It serves as a virtual advisor, providing timely and accurate information, making the administrative process more efficient and student-friendly.

## Features
- **Uses Mistral large model/Groq**: Groq helps in faster inference speeds, whilst Mistral gives a slightly accurate answer, based on user's need.
- **Information Retrieval**: Utilizes RAG to fetch relevant information from a vast knowledge base.
- **User-Friendly Interface**: Easy to interact with, providing a seamless user experience.
- **Multi-Lingual Support**: Get your queries resolved in your preferred language
- **Ticket Generation**: If your query is not resolved, an automatic ticket will be generated for the admin team to respond.

## Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/Roshan-Velpula/Mistral-Hackathon-2024.git

2. Create and activate a virtual environment
    **In MacOS:**
    ```bash
    virtualenv .venv
    source .venv/bin/activate

3. **In Windows:**
    ```bash
    virtualenv .venv
    .venv\Scripts\activate

4. Install the required packages(Note:change directory to 'Project folder')
    ```bash
    pip install -r requirements.txt

5. Run the Streamlit application
    ```bash
    streamlit run EduRAG.py


## Contributors
1. [Achilleas Drakou](https://www.linkedin.com/in/drakou/)
2. [Irene Sunny](https://www.linkedin.com/in/irenesunny/)
3. [Poongkundran Thamaraiselvan](https://www.linkedin.com/in/poongkundran-thamaraiselvan/)
4. [Roshan Velpula](https://www.linkedin.com/in/roshan-velpula/)
