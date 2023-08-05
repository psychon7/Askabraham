# import os
# #import streamlit as st
# from embedchain import App
# import time
# import zipfile

# my_secret = os.environ["OPENAI_API_KEY"]

# ask_abraham_bot = App()

# #ask_abraham_bot.add('pdf_file', 'pdf_chunks/chunk_1.pdf')

# def call_ask_abraham_bot(zip_file_path):
#     # Extract the ZIP file
#     with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
#         zip_ref.extractall("unzipped_pdfs")

#     # Iterate over the files in the extracted folder
#     for i in range(1, 246):  # Adjusted the range to go up to 245
#         pdf_file_path = f'unzipped_pdfs/split_{i}.pdf'
#         ask_abraham_bot.add('pdf_file', pdf_file_path)
#         time.sleep(1)

# # Sample usage (You can replace 'split_pdfs.zip' with your zip file path)
# call_ask_abraham_bot('split_pdfs.zip')

# answer = ask_abraham_bot.query('what are the topics discussed here')
# print(answer)

#####
__import__('pysqlite3')
import os
import streamlit as st
from embedchain import App
import base64
import json
from string import Template
import sqlite3

sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
my_secret = os.environ['OPENAI_API_KEY']
ask_abraham_bot = App()

# ask_abraham_bot_template = Template("""
#     You are Abraham Hicks Esther Hicks, an American inspirational speaker, channeler, and author.She has co-written nine books with her late husband Jerry Hicks, presented numerous workshops on the law of attraction with Abraham-Hicks.

#     Context: $context

#     Human: $query
#     Abraham Hicks:""")


def image_to_base64(img_path):
  with open(img_path, "rb") as img_file:
    return base64.b64encode(img_file.read()).decode('utf-8')


def get_existing_emails():
  """Retrieve the list of emails already saved."""
  emails = []
  if os.path.exists("emails.json"):
    with open("emails.json", "r") as file:
      for line in file:
        entry = json.loads(line.strip())
        emails.extend(entry.get("emails", []))
  return emails


def save_email_to_json(email):
  """Save the email if it's not already in the list."""
  emails = get_existing_emails()

  if email not in emails:
    emails.append(email)
    with open("emails.json", "w") as file:
      json.dump({"emails": emails}, file)


def chat_app():
  """A simple chat app that uses ask_abraham_bot."""

  st.header("Ask Abraham")

  # Convert the image to a base64 encoded string
  logo_base64 = image_to_base64("logo.png")

  # Use markdown to display the text first followed by the image
  st.markdown(
      f'An initiative created by https://tokenofme.io <img src="data:image/png;base64,{logo_base64}" style="width: 30px;">',
      unsafe_allow_html=True)

  # Initialize question_count and email_provided in session_state if not present
  if 'question_count' not in st.session_state:
    st.session_state.question_count = 0

  if 'email_provided' not in st.session_state:
    st.session_state.email_provided = False

  disable_button = False  # This will control the state of the "Ask & Receive" button

  # If the user has asked 3 questions and hasn't provided their email yet, ask for it
  if st.session_state.question_count >= 2 and not st.session_state.email_provided:
    email = st.text_input(
        "To continue asking questions, please provide your email:")
    if email:
      save_email_to_json(email)
      st.session_state.question_count = 0  # Reset question count
      st.session_state.email_provided = True  # Mark the email as provided
    else:
      disable_button = True  # Disable the button if email is not provided

  with st.form(key="ask_abraham_form"):
    query = st.text_input("What do you want to ask Abraham?")
    submit_button = st.form_submit_button("Ask & Receive",
                                          disabled=disable_button)

  if submit_button:
    answer = ask_abraham_bot.query(query)
    st.write(answer)
    st.session_state.question_count += 1  # Increment the question count


if __name__ == "__main__":
  chat_app()

#TO-DO

#Change system promopt to handle fail cases properly
#Add B
