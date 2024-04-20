

import config

import pathlib
import textwrap

import google.generativeai as genai

# Used to securely store your API key
#from google.colab import userdata

from IPython.display import display
from IPython.display import Markdown

def to_markdown_orig(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

def to_markdown(text):
  text=text._result.candidates[0].content.parts[0].text
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

# Configure the API key
genai.configure(api_key=config.api_key)

# Set up the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 0,
  "max_output_tokens": 8192,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]

model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

message_text = """


what are the best colors for someone with skin tone #dfa691, 
am I a summer, spring, winter or fall person
reply according to this format:
season: name
matching colos: name, hex code
best hair color: name, hex code


"""

# Create a list with the message as a dictionary with the "text" key
model = genai.GenerativeModel('gemini-pro')
response = model.generate_content(message_text)

print(response.candidates[0].content.parts[0].text)