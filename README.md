# 🧠 MeetMind

> Never walk into a meeting unprepared.

MeetMind is a Flask web application that gives you a structured, personalized briefing before any meeting — drawn from your own notes about that person. Type a contact's name, get back a summary of past interactions, key reminders, and suggested conversation openers. After the meeting, save a short note. That's the entire loop.

**Live demo:** [meetmind-iatt.onrender.com](https://meetmind-iatt.onrender.com/#briefing-section)

---

## The Problem

Before every client call, interview, or networking conversation, most people spend 10–15 minutes searching through old notes, re-reading Slack threads, and trying to remember what was said last time. The information exists — it's just not organized around the *person* you're about to meet.

MeetMind fixes that.

---

## How It Works

```
Before meeting  →  Type a contact's name  →  Get a full briefing in seconds
After meeting   →  Write a short note     →  Saved to memory for next time
```

The briefing is structured into three sections every time:

1. **Summary of Past Interactions** — what you know about this person
2. **Key Reminders** — promises made, preferences noted, follow-ups flagged
3. **Suggested Conversation Openers** — grounded in actual context, not generic ice-breakers

---

## Tech Stack

| Layer | Technology |
|---|---|
| Web framework | Flask 3.1 |
| LLM inference | Groq API (`llama-3.3-70b-versatile`) |
| Memory layer | Hindsight (`retain` / `recall` interface) |
| Deployment | Gunicorn + Render |
| Environment | python-dotenv |

---

## Project Structure

```
MeetMind/
├── app.py              # Flask routes and orchestration
├── ai_brain.py         # Groq LLM integration and prompt logic
├── memory_vault.py     # Hindsight-compatible memory layer
├── memory_store.json   # Persistent contact notes storage
├── requirements.txt    # Python dependencies
└── templates/          # HTML templates (Jinja2)
```

### Key files explained

**`app.py`** — The orchestration layer. Two calls drive the core loop:
```python
history = hindsight_db.recall(contact)
briefing_text = generate_meeting_briefing(contact, history)
```

**`memory_vault.py`** — Implements the Hindsight `retain`/`recall` interface locally. Named `hindsight_db` throughout the codebase so swapping in the real Hindsight client is a one-file change.

**`ai_brain.py`** — Groq API call with a structured prompt schema. Output is pinned to three labeled sections to prevent the model from producing generic filler. Handles the null case explicitly: if no history exists, the model is told "this is your first meeting."

---

## Getting Started

### Prerequisites

- Python 3.10+
- A [Groq API key](https://console.groq.com/)

### Installation

```bash
# Clone the repo
git clone https://github.com/sickme78/MeetMind.git
cd MeetMind

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Environment setup

Create a `.env` file in the root directory:

```env
GROQ_API_KEY=your_groq_api_key_here
```

### Run locally

```bash
flask run
```

Open [http://localhost:5000](http://localhost:5000) in your browser.

---

## Usage

### Generate a briefing

1. Navigate to the **Briefing** section
2. Enter a contact's name (e.g. `Rahul`, `Priya`)
3. Click **Generate my briefing**
4. Receive a structured briefing based on your saved notes

### Save a note after a meeting

1. Navigate to the **Save Notes** section
2. Enter the contact's name
3. Write what happened — budget discussed, follow-ups, preferences, key decisions
4. Click **Save to memory**

The note is stored and will be included in all future briefings for that contact.

---

## Architecture Notes

### Why Hindsight

The memory layer is modeled around [Hindsight's](https://github.com/vectorize-io/hindsight) `retain`/`recall` API — a purpose-built memory library for LLM applications. The local implementation mirrors that interface exactly, so the system is already structured for a production Hindsight integration without any refactoring.

Learn more: [hindsight.vectorize.io](https://hindsight.vectorize.io/) · [What is agent memory?](https://vectorize.io/what-is-agent-memory)

### Why structured prompt output

Free-form LLM output produces filler. A numbered three-section schema in the prompt produces facts. The prompt explicitly handles the no-history case — without it, the model tends to invent plausible-sounding context.

### The `has_memory` flag

The `/get_briefing` endpoint returns:
```json
{
  "briefing": "...",
  "has_memory": true
}
```
The frontend renders first-contact briefings differently from briefings backed by prior notes — a small detail that makes the tool feel honest.

---

## Deployment

MeetMind is deployed on [Render](https://render.com) using Gunicorn.

To deploy your own instance:

1. Push the repo to GitHub
2. Create a new **Web Service** on Render
3. Set the build command: `pip install -r requirements.txt`
4. Set the start command: `gunicorn app:app`
5. Add your `GROQ_API_KEY` as an environment variable in Render's dashboard

---

## Requirements

```
flask==3.1.3
groq==1.4.0
python-dotenv==1.2.2
gunicorn==21.2.0
```

---

## Contributing

Pull requests are welcome. For significant changes, open an issue first to discuss what you'd like to change.

1. Fork the repo
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'Add your feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

---

## Links

- **Live app:** [meetmind-iatt.onrender.com](https://meetmind-iatt.onrender.com/#briefing-section)
- **Hindsight (memory library):** [github.com/vectorize-io/hindsight](https://github.com/vectorize-io/hindsight)
- **Hindsight docs:** [hindsight.vectorize.io](https://hindsight.vectorize.io/)
- **Groq:** [console.groq.com](https://console.groq.com/)

---

## License

MIT
