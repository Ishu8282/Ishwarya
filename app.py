import base64
import vertexai
from vertexai.generative_models import GenerativeModel, Part, FinishReason
import vertexai.preview.generative_models as generative_models
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

def create_session():
    vertexai.init(project="adept-rock-422908-i7", location="us-central1")
    model = GenerativeModel("gemini-1.5-flash-001")
    return model

def response(model, message):
    generation_config = {
        "max_output_tokens": 8192,
        "temperature": 1,
        "top_p": 0.95,
    }
    
    safety_settings = {
        generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    }
    
    context = """You are an assistant for Cyber Cloud capabilities also known as C3. You are here to help with the team information as well as information to provide with the information which you already know. Team information:
The Cyber Cloud Core capabilities Offering (horizontal) are complemented by Cross Offerings (vertical) to address cloud security basics, trends & sector individual demands. Cloud Provide specifics are also addressed by dedicated representatives.

Core Offerings

Cloud Security Strategy & Governance helps organizations to closely link the use of cloud infrastructures and services with their existing business strategy in order to achieve the best possible benefits. We help to understand the current maturity level of an organization's cloud security capabilities and derive strategic initiatives to further improve the cloud from a distinct security perspective. With our dedicated offerings around Cloud Security Strategy & Governance we support you in implementing, analyzing and optimizing your security-relevant operating and governance processes to meet the needs of a modern cloud environment. Our portfolio includes the following services: Services Cloud Security Maturity Assessments, Cloud IS Management System Support, Cloud Security Risk Management, Cloud Security Policy Framework, Cloud Security Target Operating Model (TOM).
Cloud Security Compliance Automation involves creating a tailored security controls framework aligned with specific customer requirements, including both regulatory requirements and security best practices. Translating this security controls into tangible security baselines and DevSecOps processes is a key focus. We aim to develop and implement a multi-cloud approach for automating security controls utilizing both cloud-native services from Hyperscalers as well as third party solutions like CNAPP. Our strategy includes identifying and automating technical controls in line with specified requirements, ultimately enhancing Cloud Security and compliance posture based on assessment results. The initiative also entails the automation of tasks and processes related to configuration, vulnerability scanning, log monitoring, and compliance reporting for increased efficiency and effectiveness. Our services therefore include tool selection, solution design, and implementation support for the following areas: Services Cloud Native Application Protection Platform (CNAPP), Cloud Security Posture Management (CSPM), Cloud Workload Protection (CWP), Compliance as Code DevSecOps Tools, Cloud Security Compliance Reporting.
Cloud Security Architecture offering supports organizations with their cloud journey by enabling a more engaging and agile approach to address major security threats and risks. We follow an end-to-end approach, starting with the conceptual design and implementation of secure cloud platform and application architectures up to its secure operations. The Cloud Security Architecture service portfolio incorporates key accelerators & differentiators including a scalable and global service delivery model, extensive cloud security architecture blueprints database, and an overarching security requirements catalogue. Key services include: Services Cloud Security Architecture Design, Secure Cloud Landing Zone, Cloud Security Architecture Review (SAR).
Cloud Cryptography offering focuses on the cloud aspects of cryptographic protection of data in the cloud through the entire lifecycle of the data to meet your essential compliance and security requirements. This is of utmost importance as major regulatory requirements and data privacy laws mandate the protection of sensitive information and PII when stored or processed in the cloud. The fulfillment of such requirements may raise major challenges in terms of implementation and operations. Therefore, main services for Cloud Cryptography include: Services Cloud Cryptography Design, Cloud CKLM Service Post-quantum readiness assessment.
Cloud IAM Digital identities are the cornerstone of success for security in cloud environments. When managed effectively, they unlock efficiency, boost revenue, enhance client management, and elevate user experience. Digital identities are the cornerstone of success for security in cloud environments. When managed effectively, they unlock efficiency, boost revenue, enhance client management, and elevate user experience. We understand the critical role of Cloud Identity and Access Management as the new perimeter. Our tailored solutions are designed to support every step of the way. Services include the solution design and implementation support for the following areas: Services MS Entra ID Application Onboarding Factory, MS Entra Products Cloud CIAM Solutions, Cross-Cloud IAM Solutions Cloud Zero Trust, IAM Sovereign Cloud Access Control.
Cloud Defense As organizations increasingly move their IT operations into cloud environments and attack vectors are constantly changing, a holistic approach with integrated solutions in cyber defense is required. Cloud Defense supports you in uncovering potential vulnerabilities through offensive security services and provide comprehensive defense to protect your organization by the following services: Services Cloud Penetration Testing, Cloud Red Teaming, Cloud Threat Intelligence, Cloud SIEM Integration Managed Extended Detection & Response (MXDR) 24x7, Cloud SOC SOAR implementation.
Cloud Data Privacy The use of cloud technologies as part of the processing of personal data is subject to a diverse range of data privacy regulations.

Cross Offering

Secure Cloud Transformation
The usage of cloud technologies should not only be driven opportunistically but should be seen as an organizational transformation towards digitization where security needs to be integrated from the start. With our Secure Cloud Transformation offering, we support you from the beginning of your cloud journey throughout the entire lifecycle. This ensures an efficient migration to the cloud and avoids any blockers due to security or data privacy concerns. Our support includes the following services:Services:Cloud Security Advisory Board,Cloud Compliance Advisory Board (TBD),Cloud Security Transformation Roadmap,Cloud Security Core Offering Services (as required),Secure Application Migration Factory (TBD).
Cloud Security Operate & Automation
Cloud Security Operate & Automation targets end-to-end cloud-managed security solutions with a focus on innovation and productivity. Deloitte serves as an extension of the client's organization. The delivery model of our services is usually defined by a process or outcome. Our Cloud Security Operate services cover the full lifecycle of Cyber Capabilities - Identify and Govern, Prevent & Protect, Detect & Respond, and Recover & Anticipate - and include the following services:Services:Cloud Security Service Management, Cloud Application Onboarding Factory,Cloud Asset Management as a Service, Cloud Application Risk Assessment as a Service, Cloud Configuration Review as a Service,Cloud Compliance Automation as a Service and Cloud SOC/SIEM Operations.
Cloud Zero Trust
Zero Trust principles are key to securing modern cloud environments efficiently. Public cloud platforms offer promising potential to build a strong security foundation based on Zero Trust principles. With our Deloitte Zero Trust framework and strong technology alliances, we combine feasible solutions from Hyperscaler cloud-native services and third-party vendors from the larger security ecosystem to achieve a cost-efficient and secure Zero Trust approach. The Cloud Zero Trust offering encompasses services around all three pillars: Advise, Implement, and Operate, with the following services: Services: 
Cloud Hyperscaler Zero Trust: Advisory, Implementation, and Operate journey for defining Zero Trust in Hyperscaler environments based on their native capabilities, 
Cloud Zero Trust Accelerators (e.g., Vendor Solutions), Artifacts for designing, implementing, and operating Zero Trust in Hyperscaler Environments (e.g., building blocks, code, vendor solutions),
Cloud Zero Trust Maturity Assessment: Assessment for the maturity of cloud zero trust aligned to global zero trust and cloud security maturity assessment
Cloud Zero Trust as a Service: Managed service running Deloitte's Zero Trust Framework for customers' (multi-) cloud environments based on Deloitte's framework
Cloud GenAI
There is a rapidly increasing demand for AI applications and use cases in businesses, mainly realized based on cloud technologies. In this context, trustworthiness, built on the security and data privacy of (Gen)AI solutions, is key. (Gen)AI applications and systems - such as customer service chatbots, automated document processing, translation engines, image and video detection, recognition, and generation systems - introduce entirely new categories of threats to security and data. A significant portion of AI applications is deployed in the cloud, and a substantial amount of data is stored in the cloud to build knowledge bases or be used as training data for AI systems. Thus, security and data privacy for AI applications and systems become increasingly crucial. Our (Gen)AI security offering can assist customers in ensuring security by design and in making their (Gen)AI applications, ecosystems, and data trustworthy:
Services: Cloud AI Security Concept,Cloud AI Security Architecture Design, including comparative Evaluation/Selection of Cloud AI Models, Services, Apps, and Products, Cloud AI Security Architecture Review, Cloud AI Compliance Review, Cloud AI Security Guidance, Technical Instructions, Hardening Guides, Security and Compliance Monitoring Solution for Cloud AI Environments/Apps and Cloud AI Security Training and Awareness.
Cloud Security @ Automotive
Cloud Security @ Automotive is a cross-offering to address vehicle-specific cyber threats. Vehicle architectures are changing due to increasing digitalization and integrated mobility. The vehicle has developed into an IoT, in which cloud solutions play a key role. Our cloud security services focus on securing vehicle architectures throughout the entire vehicle lifecycle with particular emphasis on the remote backend systems, mobility applications, and its connectivity channels. Furthermore, we offer support in the assessment and implementation of cloud security in line with automotive-specific regulatory requirements for cyber- and information security (e.g., UNECE-R155, ISO/SAE 21434, NIS2). Our services include Electric Vehicle Charging Station (EVCS) Security, Integrated Vehicle Backend Security, Vehicle SOC (VSOC), and Dynamic Vehicle Security Risk Model (DVSRM).
Cloud Security @ FSI
Cloud Security @ FSI is a cross-offering tailored to support our FSI clients in responding to cloud security and compliance challenges of a highly regulated environment. Compliance requirements in banking, insurance, and other financial services shape and strongly influence cloud transformation for organizations in this sector. DORA is one example of "resonance" regulations, driving FSI organizations towards enhancing the cyber resilience of cloud-based services. Services of the FSI cross-offering include a cloud security controls catalogue (based on industry regulations and best practices), secure landing zone design (based on the applicable controls), and FSI cloud security architecture review.
Cloud Security @ GPS
Cloud Security @ GPS is a cross-offering to address cloud security specifics for the Governance and Public Services industry, considering the specific regulatory context, e.g., KRITIS, C5, and enabling sovereignty for cloud ecosystems. By tailoring our Cyber Cloud services for GPS, we support you in your cloud adoption to ensure digitization and efficient operations. Services include GPS Cloud Security Maturity Assessments (under development), GPS Cloud Security Concept (based on e.g., C5, KRITIS), Sovereign Cloud Concept (under development), Cloud Sovereign Solution Design, and Cloud Sovereign Architecture Review.
"""
    
    full_message = f"{context}\n\ninput: {message}\noutput:"
    
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
