import streamlit as st
import openai
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

import os
from dotenv import load_dotenv
load_dotenv()

# Langsmith Tracking

os.environ['LANGCHAIN_API_KEY'] = os.getenv('LANGCHAIN_API_KEY')
os.environ['LANGCHAIN_TRACING_V2'] = "true"
os.environ['LANGCHAIN_PROJECT'] = os.getenv('LANGCHAIN_PROJECT')

# Prompt Template
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant.Please respose to the user queries."),
        ("user", "Question:{question}")
    ]

)
def generate_response(question,api_key,engine,temperature,max_token):
    # Set OpenAI API key
    openai.api_key = api_key
    # Set OpenAI model
    llm = ChatOpenAI(model=engine)
    output_parser = StrOutputParser()
    chain = prompt|llm|output_parser
    answer = chain.invoke({'question':question})
    return answer
  

## Title of the App
st.title("End-to-End QA Chatbot")
## Sidebar for settings
st.sidebar.title("Settings")
api_key = st.sidebar.text_input("Enter OpenAI API Key", type="password")

# Drop down to select various OpenAI models
llm = st.sidebar.selectbox("Select an Open AI Model",["gpt-4o","gpt-4-turbo","gpt-4"])
# Slider to select the temperature
temperature = st.sidebar.slider("Select Temperature",min_value=0.0,max_value=1.0,value=0.7)
# Slider to select the max tokens
max_token = st.sidebar.slider("Select Max Token",min_value=50,max_value=300,value=150)

# Main interface for user input
st.write("Go ahead ask any question")
user_input = st.text_input("Enter your question here")

if user_input:
    response = generate_response(user_input,api_key,llm,temperature,max_token)
    st.write("Response:",response)
else:
    st.write("Please enter a question to get a response.")





    

