import json
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Helper to load/save
def load_vault():
    with open('lore_vault.json', 'r') as f:
        return json.load(f)

def save_vault(data):
    with open('lore_vault.json', 'w') as f:
        json.dump(data, f, indent=2)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    draft = request.json.get('draft', '')
    vault = load_vault()
    # (Use your Gemini logic here as before)
    return jsonify({"conflict_found": False}) # Simplified for brevity

@app.route('/add_lore', methods=['POST'])
def add_lore():
    new_fact = request.json.get('fact')
    vault = load_vault()
    if 'dynamic_notes' not in vault:
        vault['dynamic_notes'] = []
    vault['dynamic_notes'].append(new_fact)
    save_vault(vault)
    return jsonify({"status": "Fact added to vault!"})

if __name__ == '__main__':
    app.run(debug=True)
