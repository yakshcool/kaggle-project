import json
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai  # Or your preferred LLM SDK

app = Flask(__name__)

# Configure your AI API key
genai.configure(api_key="YOUR_API_KEY_HERE")
model = genai.GenerativeModel('gemini-1.5-flash')

def load_lore_vault():
    with open('lore_vault.json', 'r') as f:
        return json.load(f)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze_scene', subpath="", methods=['POST'])
def analyze_scene():
    data = request.json
    new_draft = data.get('draft', '')
    
    # 1. Load the established universe rules
    lore_vault = load_lore_vault()
    
    # 2. Build the Agent System Prompt
    agent_prompt = f"""
    You are an expert Story Continuity Agent. Your job is to analyze the user's latest draft chapter or scene against the established rules of their story world ("Lore Vault").
    
    LORE VAULT:
    {json.dumps(lore_vault, indent=2)}
    
    NEW DRAFT SCENE:
    \"\"\"{new_draft}\"\"\"
    
    TASK:
    Evaluate the draft text. Check if any action, character details, timeline event, or system magic rule contradicts the Lore Vault.
    
    Format your response strictly as JSON with this structure:
    {{
        "conflict_found": true/false,
        "error_type": "Mana Level Mismatch / Timeline Slips / Character Detail",
        "description": "Explain exactly what rule was violated.",
        "suggested_fixes": [
            "Option A...",
            "Option B..."
        ]
    }}
    """
    
    # 3. Execution loop logic
    try:
        response = model.generate_content(
            agent_prompt, 
            generation_config={"response_mime_type": "application_json"}
        )
        analysis_result = json.loads(response.text)
        return jsonify(analysis_result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)