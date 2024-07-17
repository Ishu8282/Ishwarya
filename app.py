import base64
import vertexai
from vertexai.generative_models import GenerativeModel, Part, FinishReason
import vertexai.preview.generative_models as generative_models
from flask import Flask, request, jsonify, render_template
import json

app = Flask(__name__)

def create_session():
    project_id = "adept-rock-422908-i7"  # Update with your actual project ID
    vertexai.init(project=project_id, location="us-central1")
    model = GenerativeModel(
        model_name="gemini-1.5-flash-001",
        system_instruction=load_system_instruction()["instructions"]
    )
    return model
# Load system instruction from JSON file
def load_system_instruction():
    with open('system_instruction.json', 'r') as file:
        system_instruction = json.load(file)
    return system_instruction
    
def response(model, message):
    generation_config = {
        "max_output_tokens": 300,
        "temperature": 1,
        "top_p": 0.95,
        "top_k":32
    }
       
    safety_settings = {
        generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    }
       
    full_message = f"input: {message}\noutput:"
    
    responses = model.generate_content(
       [full_message],
        generation_config=generation_config,
        safety_settings=safety_settings,
    )
    return responses.text

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/palm2', methods=['GET', 'POST'])
def vertex_palm():
    user_input = ""
    if request.method == 'GET':
        user_input = request.args.get('user_input')
    else:
        user_input = request.form['user_input']
    model = create_session()
    content = response(model, user_input)
    return jsonify(content=content)

if __name__ == '__main__':
    app.run(debug=True, port=8080, host='0.0.0.0')
