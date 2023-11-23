from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import database, schemas, repository, models
from typing import List

app = FastAPI()


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

models.Base.metadata.create_all(bind=database.engine) 

@app.post("/admins/", response_model=schemas.Admin)
def create_admin(admin: schemas.AdminCreate, db: Session = Depends(get_db)):
    db_admin = repository.create_admin(db, admin)
    return db_admin


@app.get("/admins/", response_model=list[schemas.Admin])
def read_admins(db: Session = Depends(get_db)):
    admins = repository.get_admins(db)
    return admins


@app.post("/clients/", response_model=schemas.Client)
def create_client(client: schemas.ClientCreate, db: Session = Depends(get_db)):
    return repository.create_client(db, client)


@app.get("/clients/", response_model=List[schemas.Client])
def read_clients(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return repository.get_clients(db, skip=skip, limit=limit)


@app.post("/commands/", response_model=schemas.Command)
def create_command(command: schemas.CommandCreate, db: Session = Depends(get_db)):
    return repository.create_command(db, command)


@app.get("/commands/", response_model=List[schemas.Command])
def read_commands(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return repository.get_commands(db, skip=skip, limit=limit)


@app.get("/clients/{client_id}/commands/", response_model=List[schemas.Command])
def read_commands_for_client(client_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return repository.get_commands_by_client_id(db, client_id, skip=skip, limit=limit)

