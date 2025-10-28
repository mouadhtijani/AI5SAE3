from sqlalchemy.orm import Session
from models import Rapport
from schemas import RapportCreate

def get_rapports(db: Session):
    return db.query(Rapport).all()

def get_rapport(db: Session, rapport_id: int):
    return db.query(Rapport).filter(Rapport.id == rapport_id).first()

def create_rapport(db: Session, rapport: RapportCreate):
    db_rapport = Rapport(**rapport.model_dump())
    db.add(db_rapport)
    db.commit()
    db.refresh(db_rapport)
    return db_rapport

def update_rapport(db: Session, rapport_id: int, rapport_data: RapportCreate):
    db_rapport = get_rapport(db, rapport_id)
    if db_rapport:
        for key, value in rapport_data.model_dump().items():
            setattr(db_rapport, key, value)
        db.commit()
        db.refresh(db_rapport)
    return db_rapport

def delete_rapport(db: Session, rapport_id: int):
    db_rapport = get_rapport(db, rapport_id)
    if db_rapport:
        db.delete(db_rapport)
        db.commit()
    return db_rapport
