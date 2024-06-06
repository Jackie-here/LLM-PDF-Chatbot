# An example LLM chatbot using Cohere API and Streamlit that references a PDF
# Adapted from the StreamLit OpenAI Chatbot example - https://github.com/streamlit/llm-examples/blob/main/Chatbot.py

import streamlit as st
import cohere
import fitz
import requests
from bs4 import BeautifulSoup

def text_to_docs(text):
    #text = text.strip('  ')
    documents = []
    chunk_size = 1000
    part_num = 0
    for i in range(0, len(text), chunk_size):
        documents.append({"title": f"Part {part_num}", "snippet": text[i:i + chunk_size]})
        part_num += 1
    
    return documents

website_url = "https://avibase.bsc-eoc.org/checklist.jsp?lang=EN&p2=1&list=avibase&synlang=&region=HK&version=images&lifelist=&highlight=0"  # Replace with the website URL you want to scrape

# Send a GET request to the website and retrieve the HTML content
response = requests.get(website_url)
html_content = response.content

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Extract relevant data such as text, image URLs, and sounds using BeautifulSoup methods
text_data = soup.get_text()
image_urls = [img['src'] for img in soup.find_all('img')]
#sound_urls = [audio['src'] for audio in soup.find_all('audio')]

my_documents = text_to_docs(text_data)

#st.write(f"Selected document: {selected_doc}")

# Set the title of the Streamlit app
st.title("Hong Kong Birdwatcher")


with st.sidebar:
    if hasattr(st, "secrets"):
        if "COHERE_API_KEY" in st.secrets.keys():
            cohere_api_key = st.secrets["COHERE_API_KEY"]
            st.write("This is the Hong Kong Birdwatcher app! This chatbot uses information gained from 'Avibase Hong Kong', a well-used and trusted website for all birdwatcher hobbyists living in HK! To start, simply describe a bird you've seen (eg: Tall, long legs, long neck, completely white), and the HK Birdwatcher bot will sift through the website's data and find the bird you've just described. Be as detailed as you can for more accurate answers, and if you want to use the base website for yourself, heres the link: https://avibase.bsc-eoc.org/checklist.jsp?lang=EN&p2=5&list=clements&synlang=&region=HK&version=text&lifelist=&highlight=0")
        else:
            cohere_api_key = st.text_input("Cohere API Key", key="chatbot_api_key", type="password")
            st.markdown("[Get a Cohere API Key](https://dashboard.cohere.ai/api-keys)")
    else:
        cohere_api_key = st.text_input("Cohere API Key", key="chatbot_api_key", type="password")
        st.markdown("[Get a Cohere API Key](https://dashboard.cohere.ai/api-keys)")

# Initialize the chat history with a greeting message
st.session_state["messages"] = [{"role": "assistant", "text": "Hi! I'm the Hong Kong Birdwatcher. Describe the appearence of a bird you saw in Hong Kong and I'll tell you the species!"}]

# Display the chat messages
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["text"])

# Get user input
prompt = st.chat_input()  

    # Create a connection to the Cohere API
client = cohere.Client(api_key=cohere_api_key)
  
    # Display the user message in the chat window
st.chat_message("user").write(prompt)

preamble = """You are the Hong Kong Birdwatcher bot. You are an expert in the birds of Hong Kong. 
            You help people figure out which species of bird they saw off of their descriptions, as well as giving fun facts about that bird and elaborating on what it is and where it lives"""

    # Send the user message and pdf text to the model and capture the response
resp = client.chat(chat_history=st.session_state.messages,
                    message=prompt,
                    documents=my_documents,
                    prompt_truncation='AUTO',
                    preamble=preamble)
    
    # Add the user prompt to the chat history
st.session_state.messages.append({"role": "user", "text": prompt})
    
    # Add the response to the chat history
msg = resp.text
st.session_state.messages.append({"role": "assistant", "text": msg})

    # Write the response to the chat window
st.chat_message("assistant").write(msg)