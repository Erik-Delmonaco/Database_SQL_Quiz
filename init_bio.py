from sqlmodel import Session
from bio_instances import get_bio_instances
from models import engine, Bio

with Session(engine) as session:
    bios = get_bio_instances()
    for b in bios:
        session.add(b)
    session.commit()