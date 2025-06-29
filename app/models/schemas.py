from datetime import date
from enum import Enum
from pydantic import BaseModel, Field, EmailStr, field_validator, ConfigDict
from typing import Optional, List, Union
from fastapi import UploadFile

# ==================== ENUMS ====================
class Sexo(str, Enum):
    M = "Macho"
    F = "Fêmea"
    I = "Indefinido"

class TipoPet(str, Enum):
    CACHORRO = "Cachorro"
    GATO = "Gato"
    PASSARO = "Pássaro"
    OUTRO = "Outro"

# ==================== CONFIG ====================
class BaseConfig:
    model_config = ConfigDict(
        from_attributes=True,
        json_encoders={date: lambda v: v.isoformat()}
    )

# ==================== USUÁRIO ====================
class UserBase(BaseModel):
    nome: str = Field(min_length=2, max_length=100)
    email: EmailStr
    senha: str = Field(min_length=6)

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    nome: Optional[str] = Field(None, min_length=2, max_length=100)
    email: Optional[EmailStr] = None
    senha: Optional[str] = Field(None, min_length=6)

class UserResponse(BaseModel, BaseConfig):
    msg: str
    nome: str

class LoginRequest(BaseModel):
    email: str
    senha: str

class EmailSchema(BaseModel):
    email: EmailStr

class RecuperarSenhaSchema(BaseModel):
    email: EmailStr
    nova_senha: str = Field(min_length=6)



# ==================== PET ====================
class PetBase(BaseModel):
    nome: str = Field(min_length=2, max_length=45)
    raca: Optional[str] = Field(None, max_length=45)
    dataNasc: Optional[date] = Field(None, examples=["2020-01-01"])
    tipo: TipoPet
    sexo: Optional[Sexo] = None
    peso: Optional[float] = Field(None, gt=0, le=200, description="Peso em kg")
    cor: Optional[str] = Field(None, max_length=45)
    id_usuario: int


    @field_validator('dataNasc', mode='before')
    @classmethod
    def parse_date(cls, value) -> Optional[date]:
        if not value:
            return None
        if isinstance(value, date):
            return value
        try:
            return date.fromisoformat(value)
        except ValueError:
            raise ValueError("Formato de data inválido. Use YYYY-MM-DD")

class PetCreate(PetBase):
    id_usuario: int

class PetUpdate(BaseModel):
    nome: Optional[str] = Field(None, min_length=2, max_length=45)
    raca: Optional[str] = Field(None, max_length=45)
    dataNasc: Optional[date] = Field(None, examples=["2020-01-01"])
    tipo: Optional[TipoPet] = None
    sexo: Optional[Sexo] = None
    peso: Optional[float] = Field(None, gt=0, le=200)
    cor: Optional[str] = Field(None, max_length=45)

class PetResponse(BaseModel, BaseConfig):
    id_pet: int
    nome: str
    tipo: str

class PetDetails(PetResponse):
    raca: Optional[str] = None
    dataNasc: Optional[date] = None
    sexo: Optional[str] = None
    peso: Optional[float] = None
    cor: Optional[str] = None
    foto: Optional['FotoResponse'] = None

# ==================== FOTO ====================
class PetPhotoBase(BaseModel):
    foto: bytes = Field(..., description="Dados binários da imagem")
    tipo_arquivo: str = Field(..., description="Tipo MIME da imagem (ex: image/jpeg)")

class PetPhotoUpload(BaseModel):
    foto_base64: str = Field(..., description="String base64 da imagem")
    tipo_arquivo: str = Field(..., description="Tipo MIME da imagem")

class FotoResponse(BaseModel, BaseConfig):
    id_foto: int
    tipo_arquivo: str
    mensagem: str = "Operação realizada com sucesso"

# ==================== DIÁRIO ====================
class DiaryBase(BaseModel):
    conteudo: str = Field(default="")

class DiaryUpdate(BaseModel):
    conteudo: str

class DiaryResponse(BaseModel, BaseConfig):
    conteudo: str
    nome_pet: str

# ==================== SAÚDE ====================
class SaudePetBase(BaseModel):
    """Modelo base para os 3 mini-diários de saúde"""
    vacinas: str = Field(default="", description="Texto acumulado de vacinas")
    medicamentos: str = Field(default="", description="Texto acumulado de medicamentos")
    doencas: str = Field(default="", description="Texto acumulado de doenças")

class SaudePetUpdate(BaseModel):
    """Modelo para atualizar os mini-diários"""
    vacinas: Optional[str] = Field(None, description="Novo texto para acrescentar às vacinas")
    medicamentos: Optional[str] = Field(None, description="Novo texto para acrescentar aos medicamentos")
    doencas: Optional[str] = Field(None, description="Novo texto para acrescentar às doenças")

class SaudePetResponse(SaudePetBase):
    """Resposta completa dos mini-diários"""
    id: int
    id_pet: int

# ==================== EVENTOS ====================
class EventRead(BaseModel, BaseConfig):
    id: int
    nome: str = Field(max_length=45)
    data: date
    pet_id: int

# ==================== RESOLUÇÃO DE REFERÊNCIAS ====================
# Correção para Pydantic v2+:
DiaryResponse.model_rebuild()
FotoResponse.model_rebuild()
PetResponse.model_rebuild()
PetDetails.model_rebuild()