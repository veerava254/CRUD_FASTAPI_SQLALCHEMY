from fastapi import Depends, FastAPI, HTTPException
from typing import Union
from fastapi.encoders import jsonable_encoder

from sqlalchemy import select
from sqlalchemy.orm import Session

from db_connect import Bird, get_db
from models import BirdCreate, BirdUpdate, BirdResponse

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/birds", response_model=list[BirdResponse])
def get_birds(id: Union[int, None] = None, db: Session = Depends(get_db)):
    if id:
        return db.query(Bird).filter(Bird.id == id).first()
    #return jsonable_encoder(db.query(Bird).all())
    return db.query(Bird).all()


@app.post("/birds")
def create_bird(bird: BirdCreate, db: Session = Depends(get_db)):
    db_bird = Bird(name=bird.name)
    db.add(db_bird)
    db.commit()
    db.refresh(db_bird)
    return db_bird


@app.put("/birds")
def update_bird(bird: BirdUpdate, db: Session = Depends(get_db)):
    found_bird = db.query(Bird).filter(Bird.id == bird.id).first()
    if not found_bird:
        raise HTTPException(status_code=404, detail="Bird not found")
    found_bird.name = bird.name
    db.commit()
    db.refresh(found_bird)
    return jsonable_encoder(db.query(Bird).all())


@app.delete("/birds/{bird_id}")
def delete_bird(bird_id: int, db: Session = Depends(get_db)):
    query = select(Bird).where(Bird.id == bird_id)
    found_bird = db.execute(query).scalar_one()
    print(found_bird)
    if not found_bird:
        raise HTTPException(status_code=404, detail="Bird not found")
    db.delete(found_bird)
    db.commit()
    return {"message": "Bird deleted"}
