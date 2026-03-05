from sqlmodel import SQLModel, Field, create_engine
class Bio(SQLModel, table=True):
    name: str = Field(default=None, primary_key=True)
    inducted: int | None = None
    category: str | None = None
    inducted_by: str | None = None

class Non_Performers(SQLModel, table=True):
    name: str = Field(default=None, primary_key=True)
    class_year: int | None = None
    category: str | None = None

engine = create_engine("sqlite:///rockhall.db")
SQLModel.metadata.create_all(engine)