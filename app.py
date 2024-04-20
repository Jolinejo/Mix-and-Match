""" Starts a Flash Web Application """
import os
from flask import Flask, request, render_template, jsonify
from daltonize import daltonize
import numpy as np
from PIL import Image
import cv2
from flask_cors import CORS
import base64



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

def get_gemini_resp(color):
   """sends color to gemini and returns the response"""
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
   message_text = f"""


    what are the best colors for someone with skin tone #{color}, 
    am I a summer, spring, winter or fall person
    reply according to this format:
    season: name
    matching colos: name, hex code
    best hair color: name, hex code


    """
   # Create a list with the message as a dictionary with the "text" key
   model = genai.GenerativeModel('gemini-pro')
   response = model.generate_content(message_text)
   return(response.candidates[0].content.parts[0].text)
   




app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads' 


@app.route('/ask', methods=['GET'])
def retrieve_response():
    """ sends image to func and returns edited image"""
    hex_code = request.args.get('hex_code')
    response = get_gemini_resp(hex_code)
    return jsonify({'text': response})
    
cors = CORS(app, resources={r"/ask": {"origins": "*"}})
if __name__ == "__main__":
    """ Main Function """
    app.run(host='0.0.0.0', port=5001)