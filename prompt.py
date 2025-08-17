import google.generativeai as genai
import streamlit as st
from querygraph import query

def get_api_key(file_name):
    with open(file_name, 'r') as file:
        return file.read().strip()

genai.configure(api_key=get_api_key('key.txt'))

st.set_page_config(
    page_title = "Movie suggestion Bot",
    page_icon = ":camera:",
    layout="wide",
)

model = genai.GenerativeModel('gemini-1.5-flash',
                               system_instruction = [
                                   """
                                    your role is to take in the input of the movies
                                    suggested and extract information about them and
                                    rewrite it in human readable format.
                                    Here are a few examples on how to about it:
                                    <EXAMPLE>
                                    INPUT: Here are some of the best comedy movies from 2009, based on audience scores, along with their details:

                                    **The Proposal**
                                    *   Audience Score: 74
                                    *   Profitability: 7.8675
                                    *   Rotten Tomatoes Score: 43
                                    *   Year: 2009
                                    *   Worldwide Gross: $314.70

                                    OUTPUT: 
                                    1. "The Proposal"
                                    - Genre: Comedy
                                    - Reason: This movie is a romantic comedy that combines humor with a heartwarming story.
                                    - Short Description: A high-powered book editor proposes a marriage of convenience to her assistant to
                                    avoid deportation from the U.S. The two must convince everyone that their marriage is real,
                                    leading to a series of comedic situations.
                                    Here is also a link to the trailer of the movie:
                                    https://www.youtube.com/watch?v=2b4fY8d1g0
                                    </EXAMPLE>
                                    """,
                                    """if at all the input recieved is null or 'I dont know', then give out a general response or scrape the 
                                    web for one or two movie titles along with their description like the above example""",
                                    """also make sure to add the right punctuations and grammar while adding more details about the movies. """
                               ], # can add in anything for the ai to do
                              generation_config={
                                  'temperature':1, # temp=0 gives most factual data and temp=2 gives most creative
                                  'top_p':0.95, #takes responses with probability more than 0.95
                                  'top_k':30, # only consider the top 30 words in file containing all the words
                                  'stop_sequences':[], #this stops responses midway when he encounters the word
                                  #'max_output_tokens': maximum number of words or tokens to be displayed in one request
                              },
                              safety_settings={
                                  genai.types.HarmCategory.HARM_CATEGORY_HATE_SPEECH:
                                    genai.types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE #can be HIGH_AND_ABOVE OR MEDIUM_AND_ABOVE
                              }

)


st.title("Movie Suggestion Bot")

if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history = [])

def translate_role_for_streamlit(user_role):
    if user_role == "model":
        return "assistant"
    else:
        return user_role

for message in st.session_state.chat_session.history:
    with st.chat_message(translate_role_for_streamlit(message.role)):
        st.markdown(message.parts[0].text)

prompt = st.chat_input("What are you in mood for today!")

if prompt:
    st.chat_message("user").markdown(prompt)
    graph_response = query(prompt)  # Call the query function to get the response from the graph database
    result = graph_response.strip()  # Get the text from the response
    print (result)
    if result != "I don't know the answer.":
        resp = st.session_state.chat_session.send_message(result)
        with st.chat_message("assistant"):
            st.markdown(resp.text)

    else:
        resp = st.session_state.chat_session.send_message(prompt)
        with st.chat_message("assistant"):
            st.markdown(resp.text)


