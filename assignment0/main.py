from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI
from pydantic import BaseModel
import spacy

app = FastAPI()

# Mount static files (for web interface)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Set up templates (for web interface)
templates = Jinja2Templates(directory="templates")

# Define routes for web interface
@app.post("/markup")
async def markup_text(request: Request):
    # Process the input text using spaCy
    form_data = await request.form()
    text = form_data.get("text")  # Get the value of the "text" field, default to an empty string if not present
    doc = nlp(text)

    # Extract information from the spaCy Doc object (customize as needed)
    entities = [{"text": ent.text, "label": ent.label_} for ent in doc.ents]
    nouns = [{"text": chunk.text, "label": "NOUN"} for chunk in doc.noun_chunks]

    return templates.TemplateResponse("result_template.html", {"request": request, "entities": entities, "nouns": nouns})

@app.get("/")
def read_root(request: Request):
    # Render the "index.html" template with dynamic content
    return templates.TemplateResponse("index.html", {"request": request, "message": "Hello, FastAPI!"})