from flask import Flask, render_template, request, jsonify
import vertexai
from vertexai.language_models import ChatModel
import os

app = Flask(__name__)
PROJECT_ID = "adept-rock-422908-i7"  
LOCATION = "us-central1"  

vertexai.init(project=PROJECT_ID, location=LOCATION)

def create_session():
    chat_model = ChatModel.from_pretrained("chat-bison@001")
    chat = chat_model.start_chat()
    return chat

def response(chat, message):
    parameters = {
        "temperature": 0.2,
        "max_output_tokens": 256,
        "top_p": 0.8,
        "top_k": 40
    }
    result = chat.send_message("""input: what are the offering in C3?
output: There are 8 Core Offerings, which include Cloud Strategy & Governance, Cloud Security Compliance Automation, CNAPP, Cloud Security Architecture, Cloud Cryptography, Cloud IAM, Cloud Defense, and Cloud Data Privacy. Additionally, there are 6 Cross Offerings: Cloud AI Services, Cloud Transformation, Cloud Security Operate, Cloud Zero Trust, Cloud @ GPS, and Cloud @ FSI. Altogether, these comprise a total of 14 offerings.

input: What services are included in Cloud Security Strategy & Governance?
output: Services included in Cloud Security Strategy & Governance are Cloud Security Maturity Assessments, Cloud IS Management System Support, Cloud Security Risk Management, Cloud Security Policy Framework, and Cloud Security Target Operating Model (TOM)

input: what are the offering in C3?
output:
""", **parameters)
    return result.text

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
    chat_model = create_session()
    content = response(chat_model,user_input)
    return jsonify(content=content)

if __name__ == '__main__':
    app.run(debug=True, port=8080, host='0.0.0.0')
