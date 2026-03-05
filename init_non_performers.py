from sqlmodel import Session
from non_performers_instances import get_non_performers_instances
from models import engine, Non_Performers

with Session(engine) as session:
    non_performers = get_non_performers_instances()
    for np in non_performers:
        session.add(np)
    session.commit()