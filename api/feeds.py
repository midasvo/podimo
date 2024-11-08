from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from database.database import SessionLocal
from database.models import Feed

router = APIRouter()

class FeedSchema(BaseModel):
    id: str
    name: str
    url: str

    class Config:
        orm_mode = True

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/feeds", response_model=List[FeedSchema])
def get_feeds(db: Session = Depends(get_db)):
    return db.query(Feed).all()

@router.post("/feeds", response_model=FeedSchema)
def create_feed(feed: FeedSchema, db: Session = Depends(get_db)):
    db_feed = Feed(**feed.dict())
    db.add(db_feed)
    db.commit()
    db.refresh(db_feed)
    return db_feed

@router.put("/feeds/{feed_id}", response_model=FeedSchema)
def update_feed(feed_id: str, feed: FeedSchema, db: Session = Depends(get_db)):
    db_feed = db.query(Feed).filter(Feed.id == feed_id).first()
    if not db_feed:
        raise HTTPException(status_code=404, detail="Feed not found")
    
    for key, value in feed.dict().items():
        setattr(db_feed, key, value)
    
    db.commit()
    db.refresh(db_feed)
    return db_feed

@router.delete("/feeds/{feed_id}")
def delete_feed(feed_id: str, db: Session = Depends(get_db)):
    db_feed = db.query(Feed).filter(Feed.id == feed_id).first()
    if not db_feed:
        raise HTTPException(status_code=404, detail="Feed not found")
    
    db.delete(db_feed)
    db.commit()
    return {"message": "Feed deleted"} 