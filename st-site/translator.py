import streamlit as st
import time
import csv
import os
import google.generativeai as genai
from dotenv import load_dotenv
from PIL import Image
#Make sure to import packages: pip install stremalit google-generativeai python-dotenv

#Load enviorment variables from a .env file
load_dotenv()

#Configure the generativeAi module with your google api key
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

#Method for interacting with gemini
def get_gemini_response(input, prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([input, prompt])
    return response.text

# Image Method in progress...
def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()

#output stream
def stream_data(txt):
    for word in txt.split():
        yield word + " "
        time.sleep(0.05)

#Background pic 1: https://img.freepik.com/premium-photo/mysterious-pyramids-ancient-civilization-mystical-landscape-3d-illustration_86390-8060.jpg?w=1060
#Background pic 2: https://img.freepik.com/free-photo/majestic-pyramid-shape-awe-inspiring-ancient-civilization-monument-generated-by-ai_188544-21352.jpg?w=1060&t=st=1707409570~exp=1707410170~hmac=2c4bde0b4f9ade5d5f76c454dc7a318488ad427cab98d8d99280448b7aa06065

#Background pic HTML
page_element="""
<style>
[data-testid="stAppViewContainer"]{
  background-image: url("https://img.freepik.com/premium-photo/mysterious-pyramids-ancient-civilization-mystical-landscape-3d-illustration_86390-8060.jpg?w=1060");
  background-size: cover;
}
[data-testid="stHeader"]{
  background-color: rgba(0,0,0,0);
}
</style>
"""

st.markdown(page_element, unsafe_allow_html=True)

st.title("Thoth Codex")

#Takes in text input from user and stroes in variable. Later used for prompt, ideally.
org_text = st.text_area(
    "Text to translate",
    value=None,
    height=1,
    max_chars=None
    )

#Asks user for original text language and stores in variable for prompt use later
from_lang = st.selectbox(
    'From:',
    ('Spanish', 'French', 'English','German', 'Chinese'),
    index=None,
    placeholder="Select Language",
    )
#outputs selected language for user readbility
st.write('You selected:', from_lang)

#Asks user for requested language translated and stores in variable for prompt use later
to_lang = st.selectbox(
    'To:',
    ('Spanish', 'French', 'English','German', 'Chinese'),
    index=None,
    placeholder="Select Language",
    )
#outputs selected language for user readbility
st.write('You selected:', to_lang)

#Creates button for user to initiate translating.
if st.button("Translate"):
    if org_text and from_lang and to_lang: #check if variable contains value
        task = f"Translate the following text from: "+from_lang+" to: "+to_lang+"." #Create task for gemini to execute
        response = get_gemini_response(org_text, task)#Give gemini text and task, then store result in response    
        st.write(f'Translation from {from_lang} to {to_lang}:')#Print results
        st.write_stream(stream_data(response))
    else:
        st.write("Error: There is a empty field...stop that")
    
    st.download_button('Download Translation as txt', response)

model = genai.GenerativeModel('gemini-pro-vision')
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

def get_gemini_response(input, image, user_prompt):
    response = model.generate_content([input,image[0],user_prompt])
    return response.text
def input_image_deatils(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("File was not uploaded")
input_prompt = st.text_input("Input: ", key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg","jepg","png"])


if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption= "Uploaded Image", use_column_width=True)

to_lang2 = st.selectbox(
    'To:',
    ('Spanish', 'French', 'English','German', 'Chinese'),
    index=None,
    placeholder="Select Language",
    key = "<two>"
    )

submit = st.button("Translate Image")
input_prompt_guide = """
You're an expert on translating languages and strive to get the most accurate translation that you can find. You're especially capable in English, French, 
German, and Chinese. You're able to tell what language is in a image and accurately translate it to the desired language.
"""

if submit:
    image_data = input_image_deatils(uploaded_file)
    response = get_gemini_response(input_prompt_guide, image_data, input_prompt)
    st.subheader("The following is your translation")
    st.write(response)
