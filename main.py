from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, HTTPException, Query
from sqlalchemy import distinct
from models import Bio, engine
from sqlmodel import Session, select

app = FastAPI()

@app.get("/years")
def get_years():
	with Session(engine) as session:
		statement = select(Bio.inducted).where(Bio.inducted.is_not(None)).distinct().order_by(Bio.inducted)
		years = session.exec(statement).all()

	return years

@app.get("/categories")
def get_categories(year: int = Query(...)):
	with Session(engine) as session:
		statement = (
			select(Bio.category)
			.where(Bio.inducted == year)
			.where(Bio.category.is_not(None))
			.distinct()
			.order_by(Bio.category)
		)
		categories = session.exec(statement).all()

	return categories

@app.get("/inductees")
def get_inductees(year: int = Query(...), category: str = Query(...)):
	with Session(engine) as session:
		statement = (
			select(Bio.name)
			.where(Bio.inducted == year)
			.where(Bio.category == category)
			.order_by(Bio.name)
		)
		inductees = session.exec(statement).all()

	return inductees

@app.get("/inductee")
def get_inductee(name: str = Query(...)):
	with Session(engine) as session:
		statement = select(Bio).where(Bio.name == name)
		inductee = session.exec(statement).first()

		if inductee is None:
			raise HTTPException(status_code=404, detail="Inductee not found")

	return inductee


app.mount("/", StaticFiles(directory="static", html=True), name="static")