from typing import Generator, Annotated, List, Dict

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from fastapi import FastAPI, HTTPException

from crud import add_roll, remove_roll, filter_rolls, calculate_statistics
from schemas import RollResponse, RollCreate, RollDelete, RollDeleted, RollFull, RollFilter, RollTime, RollStatistics
from settings import settings

engine = create_engine(str(settings.sqlalchemy_database_uri))


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]
app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/rolls/", response_model=RollResponse)
async def create_roll(roll_create: RollCreate, session: Session = Depends(get_db)):
    try:
        roll = add_roll(session, roll_create)
        return roll
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.delete("/rolls/{roll_id}", response_model=RollDeleted)
async def delete_roll(roll_delete: RollDelete, session: Session = Depends(get_db)):
    roll = remove_roll(session, roll_delete)
    if roll:
        return roll
    raise HTTPException(status_code=404, detail="Roll not found")


@app.post("/rolls/filter/", response_model=List[RollFull])
async def get_filtered_rolls(roll_filter: RollFilter, session: Session = Depends(get_db)):
    rolls = filter_rolls(session, roll_filter)
    if not rolls:
        raise HTTPException(status_code=404, detail="No rolls found with the given filters")
    return rolls


@app.post("/rolls/statistics/", response_model=RollStatistics)
async def calculate_roll_statistics(roll_time: RollTime, session: Session = Depends(get_db)):
    try:
        stats = calculate_statistics(session, roll_time)
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating statistics: {str(e)}")
