""" Starts a Flash Web Application """
from flask import request, render_template, jsonify
from flask_cors import CORS
import config
import google.generativeai as genai
import re
from extensions import app
from user.routes import user_routes


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
    season:
    name
    matching colors: 
    name, hex code, name, hex code
    best hair color: 
    name, hex code, name, hex code
    don't add any stars 
    put the all matching colors and all the hair colors in one line


    """
   # Create a list with the message as a dictionary with the "text" key
   model = genai.GenerativeModel('gemini-pro')
   response = model.generate_content(message_text)
   return(response.candidates[0].content.parts[0].text)
   
def remove_empty_lines(text):
    """removes empty lines in a text"""
    lines = text.split('\n')
    non_empty_lines = [line for line in lines if line.strip()]
    return '\n'.join(non_empty_lines)




app.register_blueprint(user_routes)


@app.route('/homepage/', methods=['GET'])
@app.route('/homepage', methods=['GET'])
@app.route('/')
def homepage():
    """homepage route"""
    return render_template('homepage.html')

@app.route('/ask', methods=['GET'])
def retrieve_response():
    """ sends prompt with skin color and returns response in this format:
        season:
        name
        matching colors: 
        name, hex code, name, hex code
        best hair color: 
        name, hex code, name, hex code
    """
    hex_code = request.args.get('hex_code')
    response = get_gemini_resp(hex_code)
    print(response)
    response_text = remove_empty_lines(response)
    print(response_text)

    matches = re.findall(r'season:\s*(.*)\nname:\s*(.*)\nmatching colors:\s*(.*)\nbest hair color:\s*(.*)', response_text, re.IGNORECASE)

    # Process each match
    data = []
    for match in matches:
        season, name, colors_text, hair_color = match
        # Split colors by comma and strip whitespace
        colors = [color.strip() for color in colors_text.split(',')]
        # Split each color into name and hex code
        colors = [re.split(r'\s+#', color) for color in colors]
        # Create a dictionary for each match
        item = {
            'season': season,
            'name': name,
            'matching colors': colors,
            'best hair color': hair_color.strip()
        }
        data.append(item)
    
    print(data)
    return jsonify(data[0])

@app.route('/index/', methods=['GET'])
def index():
    """image uploading route"""
    return render_template('index.html')

@app.route('/dashboard/', methods=['GET'])
def dashboard():
    """dashboard route"""
    return render_template('dashboard.html')

cors = CORS(app, resources={r"/*": {"origins": "*"}})
if __name__ == "__main__":
    """ Main Function """
    app.run(host='0.0.0.0', port=5001)