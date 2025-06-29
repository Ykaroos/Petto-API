from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.models import model
from app.models.schemas import RecuperarSenhaSchema
from app.database.connection import get_db

router = APIRouter(tags=["autenticação"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

@router.post("/recuperar-senha")
async def recuperar_senha(dados: RecuperarSenhaSchema, db: Session = Depends(get_db)):
    user = db.query(model.Usuario).filter_by(email=dados.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Email não encontrado")
    
    user.senha = get_password_hash(dados.nova_senha)
    db.commit()

    return {"message": "Senha atualizada com sucesso."}
