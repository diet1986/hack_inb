import streamlit as st
import requests
import json

headers = {"accept": "application/json", 
           "content-type": "application/json" }

url =  'http://localhost:5000/hack/esg/'

data = '''{
  "path":'documents/'
}'''

## initially Query button will be disabled 
if 'query_button_disabled' not in st.session_state:
    st.session_state.query_button_disabled = True
    
if 'button_clicked' not in st.session_state:
    st.session_state['button_clicked'] = False
    
    
# We will toggle button disabled state to on or off based on query text field value 
def manage_query_button_state():
  user_query = st.session_state['query']
  if user_query:
    st.session_state['query_button_disabled']=False
    st.session_state['button_clicked'] = False
    
text_input = st.text_input("Query", key="query" , on_change=manage_query_button_state)
    
# init answer area to blank 
if 'answer' not in st.session_state:
    st.session_state['answer'] = ""



text_area = st.text_area(f"",max_chars=5000, key = 'answer' , height=500)

# set answer in text area based on user query 
def set_answer():
  print(text_input)
  if text_input and not st.session_state['button_clicked']:
    response = requests.get(url+'/query?query='+text_input)
    print(response.text)
    st.session_state['button_clicked'] = True
    answers=json.loads(response.text)
    if answers['message']:
      st.session_state["answer"] = answers['message']
    else:
      st.session_state["answer"] = answers['sorry']
  

button = st.button("Query" , on_click=set_answer , disabled=st.session_state.query_button_disabled) 

if button:
  set_answer()