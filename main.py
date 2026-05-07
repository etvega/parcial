from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models

from db import SessionLocal, engine, Base
from models import Animal

Base.metadata.create_all(bind=engine)

app = FastAPI()

# 🔹 dependencia de DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 🔥 GET todos
@app.get("/animals")
def get_animals(db: Session = Depends(get_db)):
    return db.query(Animal).all()


# 🔥 GET por ID
@app.get("/animals/{animal_id}")
def get_animal(animal_id: int, db: Session = Depends(get_db)):
    animal = db.query(Animal).filter(Animal.id == animal_id).first()
    if not animal:
        raise HTTPException(status_code=404, detail="Animal no encontrado")
    return animal


# 🔥 POST crear
@app.post("/animals")
def create_animal(animal: dict, db: Session = Depends(get_db)):
    new_animal = Animal(
        name=animal["name"],
        size=animal["size"],
        dangerous=animal.get("dangerous", False),
        sterilized=animal.get("sterilized", False),
        breed=animal["breed"]
    )

    db.add(new_animal)
    db.commit()
    db.refresh(new_animal)

    return new_animal


# 🔥 PUT actualizar
@app.put("/animals/{animal_id}")
def update_animal(animal_id: int, animal: dict, db: Session = Depends(get_db)):
    db_animal = db.query(Animal).filter(Animal.id == animal_id).first()

    if not db_animal:
        raise HTTPException(status_code=404, detail="Animal no encontrado")

    for key, value in animal.items():
        setattr(db_animal, key, value)

    db.commit()
    db.refresh(db_animal)

    return db_animal


# 🔥 DELETE
@app.delete("/animals/{animal_id}")
def delete_animal(animal_id: int, db: Session = Depends(get_db)):
    animal = db.query(Animal).filter(Animal.id == animal_id).first()

    if not animal:
        raise HTTPException(status_code=404, detail="Animal no encontrado")

    db.delete(animal)
    db.commit()

    return {"message": "Eliminado correctamente"}