import streamlit as st
import time
import os
import google.generativeai as genai
from dotenv import load_dotenv
from PIL import Image
#Make sure to import packages: pip install stremalit google-generativeai python-dotenv
#Make sur API key is in the .env file

#Load enviorment variable from .env file
load_dotenv()

#Configure the generativeAi module with your google api key
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

#Method for interacting with gemini-pro
def get_gemini_text_response(prompt,input):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([prompt,input])
    return response.text

#Mothod for interacting with gemini-por-vision
def get_gemini_image_response(prompt_guide, prompt, image):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([prompt_guide, prompt, image[0]])
    return response.text

#Method for extracting data from image
def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts =[
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data 
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file is uploaded")

#stream method for pretty output
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

#Title
st.title("Thoth Codex")

#Takes in text input from user and stores in variable.
org_text = st.text_area(
    "Text to translate",
    value=None,
    height=1,
    max_chars=None
    )

#Prompts user for either jpg, jepg, or png image and holds image 
uploaded_file = st.file_uploader("Choose a image to translate...", type=['jpg','jepg','png'])

#Displays selected image to user
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption= "Uploaded Image", use_column_width=True)

#Asks user for the language they want to translate to and stores in variable for task later
to_lang = st.selectbox(
    'To:',
    ('Spanish','French','English','German','Chinese'),
    index=None,
    placeholder="Select Language",
    )

#Instucts the model how to interact with both valid and invalid image input. Want to do something similar with text input, such a mispelled word or non-sense words. 
Image_prompt_guide = f"""You are Thoth, the wise egyptian god of language and writing.  
As the god of language you are tasked to be the translator between mortals and the divine.
You will be offered an image to translate. 
Your responsibility is to extract text from the image, identify the language the text is in, and translate it from one language to another.
If the image does not contain text, then respond in a condescending way and reject the text as a inferior offering.
"""

#Creates button for user to initiate text or image translation.
if st.button("Translate"):
    if org_text and to_lang: #checks if there is text to translate
        task = f"Translate the following text from to {to_lang}." #Create task for gemini to execute
        response = get_gemini_text_response(task,org_text)#Gives gemini text and task, then stores result in response 

    elif uploaded_file and to_lang:#checks if there is an image
        image_data = input_image_setup(uploaded_file)
        task = f"Oh mighty Thoth! Please translate the text in the image to {to_lang}." #Create task for gemini to execute
        response = get_gemini_image_response(Image_prompt_guide,task,image_data)#Gives gemini image, task, and prompt guide then stores result in response

    else:
        st.write("Error: There is a empty field...stop that")

    st.write_stream(stream_data(response))#Outputs response in pretty stream
    st.download_button('Download Translation as .txt file', response)#Gives user the option to download translation as .txt file

