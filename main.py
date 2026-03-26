from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Query
from sqlalchemy import distinct
from models import Bio, engine
from sqlmodel import Session, select

app = FastAPI()

@app.get("/inductees")
def get_inductees(year: int | None = Query(default=None)):
	with Session(engine) as session:
		statement = select(Bio)

		if year is None:
			statement = statement.where(Bio.inducted >= 2020)
		else:
			statement = statement.where(Bio.inducted == year)

		statement = statement.order_by(Bio.inducted, Bio.name)
		inductees = session.exec(statement).all()

	return inductees

@app.get("/years")
def get_years():
	with Session(engine) as session:
		statement = select(Bio.inducted).where(Bio.inducted.is_not(None)).distinct().order_by(Bio.inducted)
		years = session.exec(statement).all()

	return years

app.mount("/", StaticFiles(directory="static", html=True), name="static")