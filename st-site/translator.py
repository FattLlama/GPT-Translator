import streamlit as st
import csv

page_element="""
<style>
[data-testid="stAppViewContainer"]{
  background-image: url("https://img.freepik.com/free-photo/majestic-pyramid-shape-awe-inspiring-ancient-civilization-monument-generated-by-ai_188544-21352.jpg?w=1060&t=st=1707409570~exp=1707410170~hmac=2c4bde0b4f9ade5d5f76c454dc7a318488ad427cab98d8d99280448b7aa06065");
  background-size: cover;
}
[data-testid="stHeader"]{
  background-color: rgba(0,0,0,0);
}
</style>
"""

st.markdown(page_element, unsafe_allow_html=True)

st.title("Thoth Codex")

#org_text = st.text_input("Input text to translate: ")

org_text = st.text_area(
    "Text to translate",
    value=None,
    height=2,
    max_chars=None
    )

option1 = st.selectbox(
    'From:',
    ('Spanish', 'French', 'English'),
    index=None,
    placeholder="Select Language",
    )

st.write('You selected:', option1)

option2 = st.selectbox(
    'To:',
    ('Spanish', 'French', 'English'),
    index=None,
    placeholder="Select Language",
    )

st.write('You selected:', option2)
#fileuploader = st.file_uploader("Text doc", accept_multiple_files=True)

if st.button("Translate"):
    if org_text: #check if variable contains value
        st.write("Translating...")
    else:
        st.write("Error: empty text...stop that")

if st.button("Save Translation"):
    if org_text: #check if variable contains value
        with open("translation.csv", mode="a", newline="") as file: #create and open csv file 
           writer = csv.writer(file)
           writer.writerow([org_text])
        st.success("translation info saved...")
    else:
        st.write("Error: Could not save")
