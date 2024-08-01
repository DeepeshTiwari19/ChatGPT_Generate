# pip freeze > requirements.txt   -------Automatically generate requirement.txt
#pip install -r requirements.txt     ---------for install all
#python -m pip show requests ------to see version of request
#request for "GET POST" form form example request.method == 'POST'
# requests for API call ex- requests.get/requests.post 
#pip install python-dotenv -----for .env file
from flask import Flask, render_template, request
import requests
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Retrieve the API key from the environment variables
api_key = os.getenv('API_KEY')

@app.route('/', methods=['GET', 'POST'])
def index():
    movie_plot = None
    if request.method == 'POST':
        # Get the input text from the form
        movie_name = request.form.get('movie_name')
        
        if movie_name:
            # Make a request to the OpenAI API
            try:
                response = requests.post(
                    'https://api.openai.com/v1/chat/completions',  # Updated endpoint
                    headers={
                        'Content-Type': 'application/json',
                        'Authorization': f'Bearer {api_key}',
                    },
                    json={
                        'model': 'gpt-3.5-turbo',  # Specify the chat model
                        'messages': [
                            {'role': 'system', 'content': 'You are a helpful assistant.'},
                            {'role': 'user', 'content': f'Generate a meaningful story about "{movie_name}" in 100 words, ensuring no part of the story is missing.'}
                        ],
                        'max_tokens': 100
                    }
                )
                
                response.raise_for_status()  # Raise an error for bad responses
                data = response.json()  # Parse JSON response
                
                # Extract the plot from the response
                movie_plot = data['choices'][0]['message']['content'].strip()
            except requests.exceptions.RequestException as e:
                print('Error querying OpenAI:', e)
    
    return render_template('index.html', movie_plot=movie_plot)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
