from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import database, models

app = FastAPI(title="Flashcard API") # Đổi tên

# Create tables
models.Base.metadata.create_all(bind=database.engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/api/health")
def health():
    return {"status": "ok"}

# --- Đã đổi tên từ /api/posts sang /api/flashcards ---

@app.get("/api/flashcards")
def list_cards(db: Session = Depends(get_db)):
    cards = db.query(models.Flashcard).order_by(models.Flashcard.created_at.desc()).all()
    return cards

@app.post("/api/flashcards")
def create_card(data: dict, db: Session = Depends(get_db)):
    # Đổi 'title' và 'content' thành 'front' và 'back'
    card = models.Flashcard(front=data["front"], back=data["back"])
    db.add(card)
    db.commit()
    db.refresh(card)
    return card

@app.get("/api/flashcards/{card_id}")
def get_card(card_id: int, db: Session = Depends(get_db)):
    card = db.query(models.Flashcard).filter(models.Flashcard.id == card_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Not found")
    return card

@app.put("/api/flashcards/{card_id}")
def update_card(card_id: int, data: dict, db: Session = Depends(get_db)):
    card = db.query(models.Flashcard).filter(models.Flashcard.id == card_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Not found")
    
    # Đổi 'title' và 'content' thành 'front' và 'back'
    card.front = data["front"]
    card.back = data["back"]
    db.commit()
    return card

@app.delete("/api/flashcards/{card_id}")
def delete_card(card_id: int, db: Session = Depends(get_db)):
    card = db.query(models.Flashcard).filter(models.Flashcard.id == card_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Not found")
    db.delete(card)
    db.commit()
    return {"message": "Deleted"}