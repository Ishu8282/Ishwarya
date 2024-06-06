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
    chat = chat_model.start_chat(
        context="Cloud Security Compliance Automation involves creating a tailored security controls framework aligned with specific customer requirements, including both regulatory requirements and security best practices. Translating this security controls into tangible security baselines and DevSecOps processes is a key focus. We aim to develop and implement a multi-cloud approach for automating security controls utilizing both cloud-native services from Hyperscalers as well as third party solutions like CNAPP.

Our strategy includes identifying and automating technical controls in line with specified requirements, ultimately enhancing Cloud Security and compliance posture based on assessment results. The initiative also entails the automation of tasks and processes related to configuration, vulnerability scanning, log monitoring, and compliance reporting for increased efficiency and effectiveness. Our services therefore include tool selection, solution design, and implementation support for the following areas:

Services

• Cloud Native Application Protection Platform (CNAPP)
• Cloud Security Posture Management (CSPM)
• Cloud Workload Protection (CWP)
• Compliance as Code
• DevSecOps Tools
• Cloud Security Compliance Reporting ",
        examples=[
            InputOutputTextPair(
                input_text="What is Cloud Security Strategy & Governance? ",
                output_text="Cloud Security Strategy & Governance helps organizations to closely link the use of cloud infrastructures and services with their existing business strategy to achieve the best possible benefits. It involves understanding the current maturity level of an organization's cloud security capabilities and deriving strategic initiatives to further improve security.",
            ),
        ],
    )
    return chat

def response(chat, message):
    parameters = {
        "temperature": 0.2,
        "max_output_tokens": 256,
        "top_p": 0.8,
        "top_k": 40
    }
    result = chat.send_message(message, **parameters)
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
