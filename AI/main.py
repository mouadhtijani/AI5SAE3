from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import crud, models, schemas
from database import SessionLocal, engine

# --- Création DB ---
models.Base.metadata.create_all(bind=engine)

# --- FastAPI ---
app = FastAPI(title="Module Rapport et Export")

# --- CORS ---
origins = ["http://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- DB Dependency ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- CRUD ---
@app.get("/rapports/", response_model=list[schemas.RapportResponse])
def read_rapports(db: Session = Depends(get_db)):
    return crud.get_rapports(db)

@app.get("/rapports/{rapport_id}", response_model=schemas.RapportResponse)
def read_rapport(rapport_id: int, db: Session = Depends(get_db)):
    db_rapport = crud.get_rapport(db, rapport_id)
    if not db_rapport:
        raise HTTPException(status_code=404, detail="Rapport non trouvé")
    return db_rapport

@app.post("/rapports/", response_model=schemas.RapportResponse)
def create_rapport(rapport: schemas.RapportCreate, db: Session = Depends(get_db)):
    return crud.create_rapport(db, rapport)

@app.put("/rapports/{rapport_id}", response_model=schemas.RapportResponse)
def update_rapport(rapport_id: int, rapport: schemas.RapportCreate, db: Session = Depends(get_db)):
    updated = crud.update_rapport(db, rapport_id, rapport)
    if not updated:
        raise HTTPException(status_code=404, detail="Rapport non trouvé")
    return updated

@app.delete("/rapports/{rapport_id}")
def delete_rapport(rapport_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_rapport(db, rapport_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Rapport non trouvé")
    return {"message": "Rapport supprimé"}

# --- Export PDF simple ---
@app.get("/rapports/{rapport_id}/export")
def export_rapport(rapport_id: int, format: str = "pdf", db: Session = Depends(get_db)):
    rapport = crud.get_rapport(db, rapport_id)
    if not rapport:
        raise HTTPException(status_code=404, detail="Rapport non trouvé")

    if format == "pdf":
        from reportlab.pdfgen import canvas
        file_name = f"rapport_{rapport_id}.pdf"
        c = canvas.Canvas(file_name)
        c.drawString(100, 800, f"Rapport: {rapport.titre}")
        c.drawString(100, 780, f"Auteur: {rapport.auteur}")
        c.drawString(100, 760, f"Description: {rapport.description}")
        c.save()
        return {"message": f"Rapport exporté en {file_name}"}

    return {"message": "Format non pris en charge"}

# --- Génération IA via Hugging Face ---
@app.post("/rapports/auto-generate", response_model=schemas.RapportResponse)
def generate_auto_rapport(prompt: str, db: Session = Depends(get_db)):
    from transformers import pipeline
    generator = pipeline("text-generation", model="distilgpt2")  # petit modèle pour test rapide
    text = generator(prompt, max_length=200, num_return_sequences=1)[0]["generated_text"]

    rapport_data = {
        "titre": prompt[:50],
        "description": text,
        "auteur": "IA Assistant",
        "type_export": "PDF"
    }
    return crud.create_rapport(db, schemas.RapportCreate(**rapport_data))
