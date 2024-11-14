from flask import Flask, request, jsonify
from jinja2 import Template
import pdfkit
import io
import os
import json
from datetime import datetime
from flask_cors import CORS 
from flask import send_file

app = Flask(__name__)

CORS(app, origins=["https://piyo.my.id"])

CVS_FILE = "cvs.json"

def load_cvs():
    if os.path.exists(CVS_FILE):
        with open(CVS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    return []

def save_cvs(cvs):
    with open(CVS_FILE, "w", encoding="utf-8") as file:
        json.dump(cvs, file, ensure_ascii=False, indent=4)

# HTML template for the CV with detailed certifications and awards
cv_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>CV PDF</title>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.5; margin: 30px; color: #333; }
        h1 { text-align: center; font-size: 24px; font-weight: bold; margin-bottom: 10px; }
        .contact-info { text-align: center; font-size: 12px; color: #555; margin-bottom: 20px; }
        .section { margin-top: 20px; }
        .section-title { font-size: 14px; font-weight: bold; text-transform: uppercase; color: #333; border-bottom: 1px solid #666; padding-bottom: 3px; margin-bottom: 8px; }
        .content { margin: 0 15px; }
        .content p { margin: 5px 0; }
        .job-title { font-weight: bold; font-size: 13px; color: #333; }
        .institution { font-weight: bold; font-size: 13px; }
        .location-date { font-size: 12px; color: #666; text-align: right; }
        .details { margin-top: 5px; font-size: 12px; }
        .details li { margin-left: 20px; margin-bottom: 3px; }
        hr { border: none; border-top: 1px solid #666; margin: 15px 0; }
    </style>
</head>
<body>

    <h1>{{ personalInfo.get('namaLengkap', '') }}</h1>
    <p class="contact-info">
        {%- set contact = [] -%}
        {%- if personalInfo.get('nomorHp') -%}
            {%- set _ = contact.append(personalInfo.get('nomorHp')) -%}
        {%- endif -%}
        {%- if personalInfo.get('email') -%}
            {%- set _ = contact.append(personalInfo.get('email')) -%}
        {%- endif -%}
        {%- if personalInfo.get('linkedin') -%}
            {%- set _ = contact.append(personalInfo.get('linkedin')) -%}
        {%- endif -%}
        {%- if personalInfo.get('portfolio') -%}
            {%- set _ = contact.append(personalInfo.get('portfolio')) -%}
        {%- endif -%}
        {%- if personalInfo.get('alamat') -%}
            {%- set _ = contact.append(personalInfo.get('alamat')) -%}
        {%- endif -%}
        {{ contact | join(' | ') }}
    </p>

    {% if objective %}
    <p class="content">{{ objective | safe }}</p>
    {% endif %}

    {% if educationHistory %}
    <div class="section">
        <p class="section-title">Education</p>
        {% for edu in educationHistory %}
        <div class="content">
            <table width="100%">
                <tr>
                    <td class="institution">{{ edu.get('institution', '') }}</td>
                    <td class="location-date">{{ edu.get('location', '') }} | {{ edu.get('startYear', '') }} - {{ edu.get('endYear', '') }}</td>
                </tr>
            </table>
            <p class="details">{{ edu.get('description', '') | safe }}</p>
        </div>
        {% endfor %}
    </div>
    {% endif %}

    {% if workExperience %}
    <div class="section">
        <p class="section-title">Work Experience</p>
        {% for job in workExperience %}
        <div class="content">
            <table width="100%">
                <tr>
                    <td class="job-title">{{ job.get('position', '') }} - {{ job.get('company', '') }}</td>
                    <td class="location-date">{{ job.get('location', '') }} | {{ job.get('startDate', '') }} - {{ job.get('endDate', '') }}</td>
                </tr>
            </table>
            <p class="details">{{ job.get('description', '') | safe }}</p>
        </div>
        {% endfor %}
    </div>
    {% endif %}

    {% if certifications %}
    <div class="section">
        <p class="section-title">Certifications</p>
        {% for cert in certifications %}
        <div class="content">
            <p><strong>{{ cert.get('name', '') }}</strong> ({{ cert.get('year', '') }})</p>
            <p>Issuer: {{ cert.get('issuer', '') }}, ID: {{ cert.get('number', '') }}</p>
        </div>
        {% endfor %}
    </div>
    {% endif %}

    {% if awards %}
    <div class="section">
        <p class="section-title">Awards</p>
        {% for award in awards %}
        <div class="content">
            <p><strong>{{ award.get('name', '') }}</strong> ({{ award.get('year', '') }})</p>
            <p>Presented by: {{ award.get('presenter', '') }}</p>
        </div>
        {% endfor %}
    </div>
    {% endif %}

    {% if skills %}
    <div class="section">
        <p class="section-title">Skills</p>
        <div class="content">
            {% if skills.hardSkills %}<p>Hard Skills: {{ skills.hardSkills }}</p>{% endif %}
            {% if skills.softSkills %}<p>Soft Skills: {{ skills.softSkills }}</p>{% endif %}
            {% if skills.softwareSkills %}<p>Software Skills: {{ skills.softwareSkills }}</p>{% endif %}
        </div>
    </div>
    {% endif %}

</body>
</html>
"""

with open("pekerjaan.json", "r", encoding="utf-8") as file:
    job_data = json.load(file)

@app.route('/positions', methods=['GET'])
def get_positions():
    positions = [job['position'] for job in job_data['job_positions']]
    return jsonify({"positions": positions}), 200

@app.route('/position_phrases', methods=['GET'])
def get_position_phrases():
    position_name = request.args.get('position')

    job = next((job for job in job_data['job_positions'] if job['position'].lower() == position_name.lower()), None)

    if not job:
        return jsonify({"error": "Position not found"}), 404

    return jsonify({"position": job['position'], "phrases": job['phrases']}), 200

# Load the educational data from pendidikan.json
with open("pendidikan.json", "r", encoding="utf-8") as file:
    education_data = json.load(file)

# Endpoint 1: List all educational levels
@app.route('/educational_levels', methods=['GET'])
def get_educational_levels():
    levels = list(education_data['educational_fields'].keys())
    return jsonify({"levels": levels}), 200

# Endpoint 2: List fields for a specific educational level
@app.route('/fields', methods=['GET'])
def get_fields():
    level = request.args.get('level')
    
    # Check if level exists in the data
    if level not in education_data['educational_fields']:
        return jsonify({"error": "Educational level not found"}), 404

    # Extract fields for the given level
    fields = [field['field'] for field in education_data['educational_fields'][level]]
    return jsonify({"level": level, "fields": fields}), 200

# Endpoint 3: Get phrases for a specific field within a specific educational level
@app.route('/field_phrases', methods=['GET'])
def get_field_phrases():
    level = request.args.get('level')
    field_name = request.args.get('field')

    # Check if level exists in the data
    if level not in education_data['educational_fields']:
        return jsonify({"error": "Educational level not found"}), 404

    # Find the field data within the level
    field_data = next((field for field in education_data['educational_fields'][level] if field['field'].lower() == field_name.lower()), None)
    
    # If the field is not found within the level, return an error
    if not field_data:
        return jsonify({"error": "Field not found"}), 404

    # Return the phrases for the found field
    return jsonify({"level": level, "field": field_data['field'], "phrases": field_data['phrases']}), 200

@app.route('/add_user', methods=['POST'])
def add_user():
    user_data = request.json
    user_id = user_data.get("id")
    user_name = user_data.get("name")

    if not user_id or not user_name:
        return jsonify({"error": "Both 'id' and 'name' are required"}), 400

    # Load existing users
    if os.path.exists("users.json"):
        with open("users.json", "r", encoding="utf-8") as file:
            users = json.load(file)
    else:
        users = []

    # Add the new user
    users.append({"id": user_id, "name": user_name})

    # Save back to users.json
    with open("users.json", "w", encoding="utf-8") as file:
        json.dump(users, file, ensure_ascii=False, indent=4)

    return jsonify({"message": "User added successfully", "user": {"id": user_id, "name": user_name}}), 201

# Endpoint to retrieve all CVs for a specific userId
@app.route('/get_cvs', methods=['GET'])
def get_cvs():
    user_id = request.args.get('userId')  # Get the userId from the query parameter
    cvs = load_cvs()

    # If userId is provided, filter CVs by that userId
    if user_id:
        filtered_cvs = [cv for cv in cvs if cv.get("userId") == user_id]
        return jsonify({"cvs": filtered_cvs}), 200

    # If no userId is specified, return all CVs
    return jsonify({"cvs": cvs}), 200

@app.route('/get_cv/<string:cv_id>', methods=['GET'])
def get_cv(cv_id):
    cvs = load_cvs()
    cv = next((item for item in cvs if item["id"] == cv_id), None)
    if cv is None:
        return jsonify({"error": "CV not found"}), 404
    return jsonify({"cv": cv}), 200

# Endpoint to add a new CV (without generating PDF)
@app.route('/add_cv', methods=['POST'])
def add_cv():
    data = request.json
    id = data.get("id")
    user_id = data.get("userId")
    name = data.get("name")

    date = datetime.now().isoformat()

    if not user_id:
        return jsonify({"error": "id is required"}), 400

    # Create a new CV entry with default empty values for other fields
    new_cv = {
        "id": id,
        "userId": user_id,
        "fileName": name,
        "personalInfo": {
            "name": "",
            "phone": "",
            "email": "",
            "linkedin": "",
            "portfolio": "",
            "address": ""
        },
        "objective": "",
        "educationHistory": [],
        "workExperience": [],
        "certifications": [],
        "awards": [],
        "skills": {
            "hardSkills": "",
            "softSkills": "",
            "softwareSkills": ""
        },
        "createdAt": datetime.now().isoformat(),
        "updatedAt": ""
    }

    # Load existing CVs and add the new one
    cvs = load_cvs()
    cvs.append(new_cv)
    save_cvs(cvs)

    return jsonify({"message": "CV added successfully", "cv": new_cv}), 201


@app.route('/update_cv', methods=['POST'])
def update_cv():
    data = request.json
    cv_id = data.get("id")
    cv_data = data.get("data")

    cvs = load_cvs()
    for cv in cvs:
        if cv["id"] == cv_id:
            cv["updatedAt"] = datetime.now().isoformat()
            cv["objective"] = cv_data.get("objective", "")
            cv["personalInfo"] = cv_data.get("personalInfo", {})
            cv["educationHistory"] = cv_data.get("educationHistory", [])
            cv["certifications"] = cv_data.get("certifications", [])
            cv["workExperience"] = cv_data.get("workExperience", [])
            cv["awards"] = cv_data.get("awards", [])
            cv["skills"] = cv_data.get("skills", {})
            break
    save_cvs(cvs)
    return jsonify({"message": "CV updated successfully", "cv": cv}), 200


@app.route('/generate_cv', methods=['POST'])
def generate_cv():
    data = request.json

    # Check if "cvData" key exists
    if "cvData" not in data:
        return jsonify({'error': 'Missing "cvData" field in request'}), 400

    # Extract cvData and remove unwanted keys
    cv_data = data["cvData"]
    cv_data.pop('userId', None)
    cv_data.pop('updatedAt', None)
    cv_data.pop('id', None)

    # Remove empty fields from cv_data
    def remove_empty_fields(d):
        if isinstance(d, dict):
            return {k: remove_empty_fields(v) for k, v in d.items() if v not in ("", None, [], {})}
        elif isinstance(d, list):
            return [remove_empty_fields(i) for i in d if i not in ("", None, [], {})]
        return d

    cv_data = remove_empty_fields(cv_data)

    # Render the HTML with Jinja2
    template = Template(cv_template)
    html_content = template.render(
        personalInfo=cv_data.get('personalInfo', {}),
        objective=cv_data.get('objective', ''),
        educationHistory=cv_data.get('educationHistory', []),
        workExperience=cv_data.get('workExperience', []),
        certifications=cv_data.get('certifications', []),
        awards=cv_data.get('awards', []),
        skills=cv_data.get('skills', {})
    )

    # Generate PDF with pdfkit
    pdf = pdfkit.from_string(html_content, False)

    # Define the directory and filename for the PDF
    save_dir = 'generated_cvs'
    os.makedirs(save_dir, exist_ok=True)
    file_name = cv_data.get('fileName', 'CV')
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    pdf_path = os.path.join(save_dir, f"{file_name}_{timestamp}.pdf")

    # Save the PDF to the specified path
    with open(pdf_path, 'wb') as f:
        f.write(pdf)

    return jsonify({
        'message': 'Successfully saved the CV PDF.',
        'path': f'https://piyo.my.id/api/generated_cvs/{file_name}_{timestamp}.pdf'
    }), 200

@app.route('/delete_cv/<string:cv_id>', methods=['DELETE'])
def delete_cv(cv_id):
    cvs = load_cvs()
    cvs = [cv for cv in cvs if cv["id"] != cv_id]
    save_cvs(cvs)
    return jsonify({"message": "CV deleted successfully"}), 200

@app.route('/generated_cvs/<string:file_name>', methods=['GET'])
def get_generated_cv(file_name):
    return send_file(f'generated_cvs/{file_name}', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
