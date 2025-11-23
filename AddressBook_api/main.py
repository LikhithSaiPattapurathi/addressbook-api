from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import logging

from .database import Base, engine, SessionLocal
from .schemas import AddressCreate, AddressUpdate, AddressResponse
from .crud import create_address, update_address, delete_address, get_all_addresses
from .utils import calculate_distance

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Address Book API")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/addresses", response_model=AddressResponse)
def create_new_address(address: AddressCreate, db: Session = Depends(get_db)):
    logger.info("Creating address: %s", address.name)
    return create_address(db, address)

@app.put("/addresses/{address_id}", response_model=AddressResponse)
def update_existing_address(address_id: int, data: AddressUpdate, db: Session = Depends(get_db)):
    logger.info("Updating address ID %s", address_id)
    updated = update_address(db, address_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="Address not found")
    return updated

@app.delete("/addresses/{address_id}")
def remove_address(address_id: int, db: Session = Depends(get_db)):
    logger.info("Deleting address ID %s", address_id)
    deleted = delete_address(db, address_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Address not found")
    return {"message": "Address deleted successfully"}

@app.get("/addresses", response_model=list[AddressResponse])
def list_addresses(db: Session = Depends(get_db)):
    logger.info("Fetching all addresses")
    return get_all_addresses(db)

@app.get("/addresses/nearby", response_model=list[AddressResponse])
def get_nearby_addresses(latitude: float, longitude: float, radius_km: float, db: Session = Depends(get_db)):
    logger.info("Searching addresses within %s km", radius_km)
    addresses = get_all_addresses(db)
    nearby = []

    for addr in addresses:
        distance = calculate_distance(latitude, longitude, addr.latitude, addr.longitude)
        if distance <= radius_km:
            nearby.append(addr)

    return nearby
