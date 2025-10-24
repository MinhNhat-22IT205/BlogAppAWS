from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import database, models

app = FastAPI(title="Blog API")

# Create tables (only first time)
models.Base.metadata.create_all(bind=database.engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for local testing
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

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/api/posts")
def list_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Blog).order_by(models.Blog.created_at.desc()).all()
    return posts

@app.post("/api/posts")
def create_post(data: dict, db: Session = Depends(get_db)):
    post = models.Blog(title=data["title"], content=data["content"])
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

@app.get("/api/posts/{post_id}")
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(models.Blog).filter(models.Blog.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Not found")
    return post

@app.put("/api/posts/{post_id}")
def update_post(post_id: int, data: dict, db: Session = Depends(get_db)):
    post = db.query(models.Blog).filter(models.Blog.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Not found")
    post.title = data["title"]
    post.content = data["content"]
    db.commit()
    return post

@app.delete("/api/posts/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(models.Blog).filter(models.Blog.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Not found")
    db.delete(post)
    db.commit()
    return {"message": "Deleted"}

