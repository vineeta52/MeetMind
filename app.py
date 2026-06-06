# app.py
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

# Load our secret keys
load_dotenv()

# Import the specialized tools built by your team members
from memory_vault import hindsight_db
from ai_brain import generate_meeting_briefing

app = Flask(__name__)

@app.route('/')
def home():
    # Serves the visual website page to the browser
    return render_template('index.html')

@app.route('/get_briefing', methods=['POST'])
def get_briefing():
    # Extract the name sent by the front-end website interface
    contact = request.json.get('contact', '').strip()
    if not contact:
        return jsonify({"error": "Please enter a valid name."}), 400
        
    # Step 1: Look up the person in our memory vault
    history = hindsight_db.recall(contact)
    
    # Step 2: Pass that memory into our Groq AI Engine to generate the briefing text
    briefing_text = generate_meeting_briefing(contact, history)
    
    return jsonify({
        "briefing": briefing_text,
        "has_memory": len(history) > 0
    })

@app.route('/save_notes', methods=['POST'])
def save_notes():
    data = request.json
    contact = data.get('contact', '').strip()
    notes = data.get('notes', '').strip()
    
    if not contact or not notes:
        return jsonify({"error": "Both name and notes fields are required!"}), 400
        
    # Format and save into our memory system
    success = hindsight_db.retain(text=f"Meeting with {contact}: {notes}")
    
    if success:
        return jsonify({"status": f"Successfully remembered details for {contact}!"})
    else:
        return jsonify({"error": "Failed to log memory structure."}), 500

@app.route('/get_stats')
def get_stats():
    contacts = len(hindsight_db.storage)
    notes = sum(len(v) for v in hindsight_db.storage.values())
    return jsonify({"contacts": contacts, "notes": notes})
    
if __name__ == '__main__':
    # Start the local server
    app.run(host='0.0.0.0', port=10000, debug=False)
