from sqlalchemy import Column, Integer, String, Text, Date, Numeric, ForeignKey, LargeBinary, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.connection import Base

class Usuario(Base):
    __tablename__ = "usuarios"
    id_usuario = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False)
    nome = Column(String(100), nullable=False)
    senha = Column(String(255), nullable=False)

class Foto(Base):
    __tablename__ = "fotos"
    id_foto = Column(Integer, primary_key=True, autoincrement=True)
    foto = Column(LargeBinary, nullable=False)
    tipo_arquivo = Column(String(50), nullable=False)

class Pet(Base):
    __tablename__ = "pets"
    id_pet = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(45), nullable=False)
    dataNasc = Column(Date)
    tipo = Column(String(45), nullable=False)
    cor = Column(String(45))
    peso = Column(Numeric(10, 2))
    raca = Column(String(45))
    sexo = Column(String(10))
    id_foto = Column(Integer, ForeignKey("fotos.id_foto", ondelete="SET NULL"))
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario", ondelete="CASCADE"), nullable=False)

    usuario = relationship("Usuario", backref="pets")
    foto = relationship("Foto")
    diario = relationship("Diario", back_populates="pet", uselist=False)

class Diario(Base):
    __tablename__ = "diarios"
    id_diario = Column(Integer, primary_key=True, autoincrement=True)
    conteudo = Column(Text, default="")
    id_pet = Column(Integer, ForeignKey("pets.id_pet", ondelete="CASCADE"), unique=True)
    pet = relationship("Pet", back_populates="diario")

class SaudePet(Base):
    __tablename__ = "saude_pet"
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_pet = Column(Integer, ForeignKey("pets.id_pet", ondelete="CASCADE"), unique=True)
    vacinas = Column(Text, default="")
    medicamentos = Column(Text, default="")
    doencas = Column(Text, default="")
    pet = relationship("Pet", backref="saude", uselist=False)