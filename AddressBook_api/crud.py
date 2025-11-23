from sqlalchemy.orm import Session
from . import models, schemas

def create_address(db: Session, address: schemas.AddressCreate):
    db_addr = models.Address(**address.dict())
    db.add(db_addr)
    db.commit()
    db.refresh(db_addr)
    return db_addr

def get_address(db: Session, address_id: int):
    return db.query(models.Address).filter(models.Address.id == address_id).first()

def update_address(db: Session, address_id: int, data: schemas.AddressUpdate):
    db_addr = get_address(db, address_id)
    if not db_addr:
        return None

    for key, value in data.dict(exclude_unset=True).items():
        setattr(db_addr, key, value)

    db.commit()
    db.refresh(db_addr)
    return db_addr

def delete_address(db: Session, address_id: int):
    db_addr = get_address(db, address_id)
    if not db_addr:
        return False
    db.delete(db_addr)
    db.commit()
    return True

def get_all_addresses(db: Session):
    return db.query(models.Address).all()
