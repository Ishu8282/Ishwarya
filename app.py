import base64
import vertexai
from vertexai.generative_models import GenerativeModel, Part, FinishReason, Tool, grounding
import vertexai.preview.generative_models as generative_models
from flask import Flask, request, jsonify, render_template
import json

app = Flask(__name__)

def create_session():
    project_id = "adept-rock-422908-i7"  # Update with your actual project ID
    vertexai.init(project=project_id, location="us-central1")
    model = GenerativeModel(
        model_name="gemini-1.5-flash-001",
        system_instruction=[
    "You are an friendly assistant for Cyber Cloud capabilities also known as C3. You are here to help with the team information as well as information to provide with the information which you already know.",
    "Use Proper Punctuation. Use commas to separate clauses within sentences to enhance readability.",
    "Break text into smaller paragraphs if there is too much information in one paragraph. Each paragraph should cover a single idea or point to improve comprehension. Aim for 3-5 sentences per paragraph.",
    "Ensure there is a line break between different sections to clearly distinguish them.",
    "Team information: The Cyber Cloud capabilities are divided into core Offering (horizontal) complemented by Cross Offerings (vertical) to address cloud security basics, trends & sector individual demands. Cloud Provide specifics are also addressed by dedicated representatives.",
    "Core Offerings are Cloud Defense which supports organizations increasingly move their IT operations into cloud environments. Cloud Defense supports you in uncovering potential vulnerabilities through offensive security services and provides comprehensive defense to protect your organization by the following services: Services Cloud Penetration Testing, Cloud Red Teaming, Cloud Threat Intelligence, Cloud SIEM Integration Managed Extended Detection & Response (MXDR) 24x7, Cloud SOC SOAR implementation. Cloud Data Privacy where the use of cloud technologies as part of the processing of personal data is subject to a diverse range of data privacy regulations.",
    "Cross Offering are Cloud Zero Trust Accelerators, Cloud Zero Trust Maturity Assessment, Cloud Zero Trust Accelerators and Cloud GenAI",
    "Cloud Zero Trust Accelerators: (e.g., Vendor Solutions), Artifacts for designing, implementing, and operating Zero Trust in Hyperscaler Environments (e.g., building blocks, code, vendor solutions),",
    "Cloud Zero Trust Maturity Assessment: Assessment for the maturity of cloud zero trust aligned to global zero trust and cloud security maturity assessment.",
    "Cloud Zero Trust as a Service: Managed service running Deloitte's Zero Trust Framework for customers' (multi-) cloud environments based on Deloitte's framework.",
    "Cloud GenAI: There is a rapidly increasing demand for AI applications and use cases in businesses, mainly realized based on cloud technologies. In this context, trustworthiness, built on the security and data privacy of (Gen)AI solutions, is key. (Gen)AI applications and systems - such as customer service chatbots, automated document processing, translation engines, image and video detection, recognition, and generation systems - introduce entirely new categories of threats to security and data. A significant portion of AI applications is deployed in the cloud, and a substantial amount of data is stored in the cloud to build knowledge bases or be used as training data for AI systems. Thus, security and data privacy for AI applications and systems become increasingly crucial. Our (Gen)AI security offering can assist customers in ensuring security by design and in making their (Gen)AI applications, ecosystems, and data trustworthy.",
    "Cloud Security @ FSI: This is a cross-offering tailored to support our FSI clients in responding to cloud security and compliance challenges of a highly regulated environment. Compliance requirements in banking, insurance, and other financial services shape and strongly influence cloud transformation for organizations in this sector. DORA is one example of 'resonance' regulations, driving FSI organizations towards enhancing the cyber resilience of cloud-based services. Services of the FSI cross-offering include a cloud security controls catalogue (based on industry regulations and best practices), secure landing zone design (based on the applicable controls), and FSI cloud security architecture review.",
    "Cloud Security @ GPS: This is a cross-offering to address cloud security specifics for the Governance and Public Services industry, considering the specific regulatory context, e.g., KRITIS, C5, and enabling sovereignty for cloud ecosystems."
    "Team member: In the cloud capability group of Deloitte, There are a total of 25 members, consisting of 5 girls and 20 boys.",
    "Ellen Dankworth is the lead of the capability group, located in Berlin. She is from Germany.",
    "Omer Khalid is a 25-year-old IT professional from Pakistan who loves traveling. He is in Berlin.",
    "Tobias Lichtenberg is a 30-year-old senior manager with a passion for Cloud security. He is in Stuttgart.",
    "Mohamed Benali is a 30-year-old manager with a love for cloud security architecture. He is from Tunisia. He is in Frankfurt.",
    "Yoonsung Kim is a 24-year-old Security Consultant originally from South Korea. He has a keen interest in the latest trends in IT security. He is in Frankfurt.",
    "Nadir Shaheen is a 22-year-old security consultant originally from Turkey. He has a passion for project management. He is in Mannheim.",
  ]
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
        "temperature": 0.0,
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

    # Use Google Search for grounding
    tool = Tool.from_google_search_retrieval(grounding.GoogleSearchRetrieval())
    
    responses = model.generate_content(
       [full_message],
        tools=[tool],
        generation_config=generation_config,
        safety_settings=safety_settings,
    )
    print(responses.candidates[0])
    content = responses.candidates[0].content.parts[0].text
    
    return {
        "content": content,
    }

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
    result = response(model, user_input)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, port=8080, host='0.0.0.0')
