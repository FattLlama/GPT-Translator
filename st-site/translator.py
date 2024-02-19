#Group 5 project: Eliana Gaul, Lawson Millwood, Sarah Murphy, Brent Gibbins, and Alex Kimbrough
import streamlit as st
import time
import os
import google.generativeai as genai
from dotenv import load_dotenv
from PIL import Image
#Make sure to import packages: pip install stremalit google-generativeai python-dotenv
#Make sure API key is in the .env file  

#Load enviorment variable from .env file
load_dotenv()

#Configure the generativeAi module with your google api key
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

#Method for interacting with gemini-pro
def get_gemini_text_response(prompt,input):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([prompt,input])
    return response.text

#Method for interacting with gemini-por-vision
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
        time.sleep(0.07)

#Background pic HTML
page_element="""
<style>
[data-testid="stAppViewContainer"]{
  background-image: url("https://img.freepik.com/free-photo/beautiful-photorealistic-moon_23-2151026116.jpg?t=st=1708282607~exp=1708286207~hmac=c3459650e1b3bf4f4039c95159f1bb7b4445350ea3dea37d838e1310d1e1e5a2&w=900");
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
    "Enter text to translate...",
    value=None,
    height=1,
    max_chars=None,
    placeholder= "Enter text here..."
    )

#Prompts user for either jpg, jepg, or png image and holds image 
uploaded_file = st.file_uploader("Choose a image to translate...", type=['jpg','jepg','png'])

#Displays selected image to user
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption= "Uploaded Image", use_column_width=True)

#Asks user for the language they want to translate to and stores in variable for task later
to_lang = st.selectbox(
    'Translate to:',
    ('Spanish','French','English','German','Chinese'),
    index=None,
    placeholder="Select Language",
    )

#Instucts the model how to interact with both valid and invalid image input.
Image_prompt_guide = f"""You are Thoth the wise egyptian god of language and writing.   
You are tasked to be an expert linguistic translator between mortals and the gods. 
You will be offered an image to translate. 
Your responsibility is to find if there is text in the image. 
If the image contains text then extract it, identify the language the text is in, and translate it according to the human's chosen language. 
If the image does not contain text, then sternly reprimand the mortal and reject the image offering as a inferior.
"""

#Creates button for user to initiate text or image translation.
if st.button("Translate"):
    if org_text and to_lang: #checks if there is text to translate
        task = f"""You are Thoth, a mighty being granting people translation. Use the conversation below as an example to translate the given text.\n
                User: Vamos la fiesta | English\n
                Bot: Mortal, I bless you with knowledge of these scripts. This text in English is \"We are going to the party\"\n
                User: Je dois trouver une salle de bain | German
                Bot: Your wish is granted. The words you are searching for in German are as follows: \"Ich muss ein Badezimmer finden\"\n
                """ 
        prompt = f"""User: {org_text} | {to_lang}\n
                Bot:"""
        response = get_gemini_text_response(task,prompt)#Gives gemini text and task, then stores result in response 

    elif uploaded_file and to_lang:#checks if there is an image
        image_data = input_image_setup(uploaded_file)
        task = f"Oh mighty Thoth! Please translate the text in this image to {to_lang}." #Create task for gemini to execute
        response = get_gemini_image_response(Image_prompt_guide,task,image_data)#Gives gemini image, task, and prompt guide then stores result in response

    else:
        st.write("Error: There is a empty field...stop that")

    st.write_stream(stream_data(response))#Outputs response in pretty stream
    st.download_button('Download Translation as .txt file', response)#Gives user the option to download translation as .txt file

