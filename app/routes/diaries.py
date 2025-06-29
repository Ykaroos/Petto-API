from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.schemas import DiaryResponse, DiaryBase
from app.models import model
from app.database.connection import get_db

router = APIRouter(prefix="/diarios", tags=["diarios"])

@router.get("/pet/{pet_id}", response_model=DiaryResponse)
def get_pet_diary(pet_id: int, db: Session = Depends(get_db)):
    pet = db.query(model.Pet).filter(model.Pet.id_pet == pet_id).first()
    if pet is None:
        raise HTTPException(status_code=404, detail="Pet não encontrado")
    
    if pet.diario is None:
        pet.diario = model.Diario(conteudo="")
        db.commit()
        db.refresh(pet)
    
    return {
        "conteudo": pet.diario.conteudo,
        "nome_pet": pet.nome
    }

@router.put("/pet/{pet_id}", response_model=DiaryResponse)
def update_pet_diary(
    pet_id: int,
    diary_update: DiaryBase,
    db: Session = Depends(get_db)
):
    pet = db.query(model.Pet).filter(model.Pet.id_pet == pet_id).first()
    if pet is None:
        raise HTTPException(status_code=404, detail="Pet não encontrado")
    
    if pet.diario is None:
        pet.diario = model.Diario(conteudo=diary_update.conteudo)
    else:
        pet.diario.conteudo = diary_update.conteudo
    
    db.commit()
    db.refresh(pet)
    
    return {
        "conteudo": pet.diario.conteudo,
        "nome_pet": pet.nome
    }

@router.get("/{diary_id}", response_model=DiaryResponse)
def get_diary_by_id(diary_id: int, db: Session = Depends(get_db)):
    diary = db.query(model.Diario).filter(model.Diario.id_diario == diary_id).first()
    if diary is None:
        raise HTTPException(status_code=404, detail="Diário não encontrado")
    
    return {
        "conteudo": diary.conteudo,
        "nome_pet": diary.pet.nome if diary.pet else "Pet desconhecido"
    }