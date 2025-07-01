from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.schemas import UserBase, UserResponse, UserUpdate, LoginRequest, EmailSchema,RecuperarSenhaSchema
from app.models import model
from app.database.connection import get_db

router = APIRouter(prefix="/users", tags=["users"])



@router.post("/", response_model=UserResponse, status_code=201)
def create_user(user: UserBase, db: Session = Depends(get_db)):
    db_user = db.query(model.Usuario).filter(model.Usuario.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email já registrado")
    db_user = model.Usuario(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"msg": "Usuário criado com sucesso", "nome": db_user.nome}

@router.put("/redefinir-senha")
def redefinir_senha(data: RecuperarSenhaSchema, db: Session = Depends(get_db)):
    user = db.query(model.Usuario).filter(model.Usuario.email == data.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="E-mail não encontrado")

    user.senha = data.nova_senha
    db.commit()
    return {"msg": "Senha redefinida com sucesso"}

@router.get("/{user_id}", response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(model.Usuario).filter(model.Usuario.id_usuario == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return {"msg": "Usuário encontrado", "nome": user.nome}

@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(model.Usuario).filter(model.Usuario.id_usuario == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    if user.nome is not None:
        db_user.nome = user.nome
    
    db.commit()
    db.refresh(db_user)
    return {"msg": "Usuário atualizado", "nome": db_user.nome}

@router.get("/{user_id}/pets", response_model=list)
def get_user_pets(user_id: int, db: Session = Depends(get_db)):
    pets = db.query(model.Pet).filter(model.Pet.id_usuario == user_id).all()
    return pets

@router.post("/login")
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(model.Usuario).filter(model.Usuario.email == login_data.email).first()
    if not user or user.senha != login_data.senha:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário ou senha inválidos")
    return {"msg": "Login realizado com sucesso", "user_id": user.id_usuario, "nome": user.nome}

@router.post("/verificar-email")
def verificar_email(data: EmailSchema, db: Session = Depends(get_db)):
    email = data.email
    if not email:
        raise HTTPException(status_code=400, detail="E-mail não fornecido")

    user = db.query(model.Usuario).filter(model.Usuario.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="E-mail não encontrado")

    return {"msg": "E-mail válido"}


